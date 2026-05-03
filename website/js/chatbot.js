/**
 * Padmashree College Chatbot Widget
 * Handles chat UI interactions and API communication
 */

// Global error handler to prevent widget from disappearing
window.addEventListener('error', (e) => {
    console.error('🚨 Global error caught:', e.error);
    console.error('Stack:', e.error?.stack);
    e.preventDefault(); // Prevent default error handling
});

// Configuration
const CONFIG = {
    API_URL: 'http://localhost:5000/chat',
    TYPING_DELAY: 1000,
    ANIMATION_DELAY: 300
};

// DOM Elements
let chatButton = null;
let chatWindow = null;
let closeChatBtn = null;
let chatInput = null;
let sendButton = null;
let chatMessages = null;

// State
let isChatOpen = false;
let isWaitingForResponse = false;
let protectionInterval = null;
let mutationObserver = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    try {
        // Initialize DOM elements
        chatButton = document.getElementById('chat-button');
        chatWindow = document.getElementById('chat-window');
        closeChatBtn = document.getElementById('close-chat');
        chatInput = document.getElementById('chat-input');
        sendButton = document.getElementById('send-button');
        chatMessages = document.getElementById('chat-messages');

        // Verify all elements exist
        if (!chatButton || !chatWindow || !closeChatBtn || !chatInput || !sendButton || !chatMessages) {
            console.error('❌ One or more chatbot elements not found!');
            console.error('chatButton:', chatButton);
            console.error('chatWindow:', chatWindow);
            console.error('closeChatBtn:', closeChatBtn);
            console.error('chatInput:', chatInput);
            console.error('sendButton:', sendButton);
            console.error('chatMessages:', chatMessages);
            return;
        }

        initializeEventListeners();
        restoreChatState();
        startProtection();
        console.log('✅ Chatbot widget initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing chatbot:', error);
    }
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    try {
        // Toggle chat window
        chatButton.addEventListener('click', (e) => {
            try {
                e.stopPropagation();
                toggleChat();
            } catch (error) {
                console.error('❌ Error in chat button click:', error);
            }
        });
        
        closeChatBtn.addEventListener('click', (e) => {
            try {
                e.stopPropagation();
                closeChat();
            } catch (error) {
                console.error('❌ Error in close button click:', error);
            }
        });

        // Send message
        sendButton.addEventListener('click', (e) => {
            try {
                e.preventDefault();
                e.stopPropagation();
                handleSendMessage();
            } catch (error) {
                console.error('❌ Error in send button click:', error);
            }
        });
        
        chatInput.addEventListener('keypress', (e) => {
            try {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage();
                }
            } catch (error) {
                console.error('❌ Error in input keypress:', error);
            }
        });

        // Auto-resize input
        chatInput.addEventListener('input', () => {
            try {
                chatInput.style.height = 'auto';
                chatInput.style.height = chatInput.scrollHeight + 'px';
            } catch (error) {
                console.error('❌ Error in input resize:', error);
            }
        });

        console.log('✅ Event listeners initialized');
    } catch (error) {
        console.error('❌ Error initializing event listeners:', error);
    }
}

/**
 * Toggle chat window open/close
 */
function toggleChat() {
    try {
        if (isChatOpen) {
            closeChat();
        } else {
            openChat();
        }
    } catch (error) {
        console.error('❌ Error toggling chat:', error);
    }
}

/**
 * Open chat window
 */
function openChat() {
    try {
        if (!chatWindow || !chatButton) {
            console.error('❌ Chat elements not found when opening');
            return;
        }
        
        // Force add active class
        chatWindow.classList.add('active');
        chatButton.classList.add('active');
        
        // Set inline styles as backup
        chatWindow.style.opacity = '1';
        chatWindow.style.visibility = 'visible';
        chatWindow.style.pointerEvents = 'all';
        chatWindow.style.transform = 'scale(1) translateY(0)';
        chatWindow.style.display = 'flex';
        
        isChatOpen = true;
        
        // Save state to localStorage
        saveChatState(true);
        
        if (chatInput) {
            chatInput.focus();
        }
        
        console.log('✅ Chat window opened (state saved)');
    } catch (error) {
        console.error('❌ Error opening chat:', error);
    }
}

/**
 * Close chat window
 */
function closeChat() {
    try {
        if (!chatWindow || !chatButton) {
            console.error('❌ Chat elements not found when closing');
            return;
        }
        
        chatWindow.classList.remove('active');
        chatButton.classList.remove('active');
        
        // Remove inline styles to allow CSS transition
        chatWindow.style.opacity = '';
        chatWindow.style.visibility = '';
        chatWindow.style.pointerEvents = '';
        chatWindow.style.transform = '';
        // Don't remove display - keep flex
        
        isChatOpen = false;
        
        // Save state to localStorage
        saveChatState(false);
        
        console.log('✅ Chat window closed (state saved)');
    } catch (error) {
        console.error('❌ Error closing chat:', error);
    }
}

/**
 * Handle sending a message
 */
async function handleSendMessage() {
    try {
        const message = chatInput.value.trim();

        // Validate message
        if (!message || isWaitingForResponse) {
            console.log('⚠️ Message empty or already waiting for response');
            return;
        }

        console.log('📤 Sending message:', message);

        // Clear input
        chatInput.value = '';
        chatInput.style.height = 'auto';

        // Add user message to chat
        addMessage(message, 'user');

        // Disable input while waiting
        setInputEnabled(false);
        isWaitingForResponse = true;

        // Show typing indicator
        const typingId = showTypingIndicator();

        try {
            // Send message to API
            const response = await sendMessageToAPI(message);

            // Remove typing indicator
            removeTypingIndicator(typingId);

            // Add bot response
            if (response.success) {
                console.log('✅ Got successful response:', response.response);
                setTimeout(() => {
                    addMessage(response.response, 'bot');
                }, CONFIG.ANIMATION_DELAY);
            } else {
                console.error('❌ API returned error:', response.error);
                setTimeout(() => {
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }, CONFIG.ANIMATION_DELAY);
            }
        } catch (error) {
            console.error('❌ Error sending message:', error);
            console.error('Error details:', error.message, error.stack);
            removeTypingIndicator(typingId);
            setTimeout(() => {
                addMessage('Sorry, I am unable to connect to the server. Please make sure the API server is running.', 'bot');
            }, CONFIG.ANIMATION_DELAY);
        } finally {
            // Re-enable input
            isWaitingForResponse = false;
            setInputEnabled(true);
            if (chatInput) {
                chatInput.focus();
            }
        }
    } catch (error) {
        console.error('❌ Critical error in handleSendMessage:', error);
        console.error('Stack:', error.stack);
        // Try to recover
        isWaitingForResponse = false;
        setInputEnabled(true);
    }
}

/**
 * Send message to chatbot API
 * @param {string} message - User message
 * @returns {Promise<Object>} API response
 */
async function sendMessageToAPI(message) {
    const response = await fetch(CONFIG.API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
}

/**
 * Add message to chat
 * @param {string} text - Message text
 * @param {string} sender - 'user' or 'bot'
 */
function addMessage(text, sender) {
    try {
        if (!chatMessages) {
            console.error('❌ Chat messages container not found!');
            return;
        }

        console.log(`📝 Adding ${sender} message:`, text);
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Handle multi-line text (preserve line breaks)
        const lines = text.split('\n');
        lines.forEach((line, index) => {
            const textP = document.createElement('p');
            textP.textContent = line || ''; // Ensure not undefined
            contentDiv.appendChild(textP);
            
            // Add spacing between paragraphs (except last one)
            if (index < lines.length - 1 && line.trim()) {
                textP.style.marginBottom = '0.5rem';
            }
        });

        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);

        console.log(`✅ Message added. Total messages: ${chatMessages.children.length}`);

        // Scroll to bottom
        scrollToBottom();
    } catch (error) {
        console.error('❌ Error adding message:', error);
        console.error('Stack:', error.stack);
    }
}

/**
 * Show typing indicator
 * @returns {string} Indicator ID
 */
function showTypingIndicator() {
    const indicatorId = 'typing-' + Date.now();
    const indicatorDiv = document.createElement('div');
    indicatorDiv.id = indicatorId;
    indicatorDiv.className = 'message bot-message';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';

    contentDiv.appendChild(typingDiv);
    indicatorDiv.appendChild(contentDiv);
    chatMessages.appendChild(indicatorDiv);

    scrollToBottom();
    return indicatorId;
}

/**
 * Remove typing indicator
 * @param {string} indicatorId - Indicator ID
 */
function removeTypingIndicator(indicatorId) {
    const indicator = document.getElementById(indicatorId);
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    try {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    } catch (error) {
        console.error('❌ Error scrolling to bottom:', error);
    }
}

/**
 * Enable/disable chat input
 * @param {boolean} enabled - Whether input should be enabled
 */
function setInputEnabled(enabled) {
    try {
        if (chatInput) {
            chatInput.disabled = !enabled;
        }
        if (sendButton) {
            sendButton.disabled = !enabled;
        }
    } catch (error) {
        console.error('❌ Error setting input enabled state:', error);
    }
}

/**
 * Handle smooth scrolling for navigation links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/**
 * Save chat state to localStorage
 */
function saveChatState(isOpen) {
    try {
        localStorage.setItem('padmashree_chat_open', isOpen ? 'true' : 'false');
        console.log(`💾 Chat state saved: ${isOpen ? 'open' : 'closed'}`);
    } catch (error) {
        console.error('❌ Error saving chat state:', error);
    }
}

/**
 * Restore chat state from localStorage
 */
function restoreChatState() {
    try {
        const savedState = localStorage.getItem('padmashree_chat_open');
        if (savedState === 'true') {
            console.log('🔄 Restoring chat state: open');
            setTimeout(() => openChat(), 100);
        }
    } catch (error) {
        console.error('❌ Error restoring chat state:', error);
    }
}

/**
 * Start protection mechanism to prevent disappearing
 */
function startProtection() {
    try {
        // Protection interval - checks every 500ms
        protectionInterval = setInterval(() => {
            // If chat should be open but active class is missing, restore it
            if (isChatOpen && chatWindow && !chatWindow.classList.contains('active')) {
                console.warn('⚠️ Chat window lost active class! Restoring...');
                chatWindow.classList.add('active');
                chatButton.classList.add('active');
                
                // Force inline styles
                chatWindow.style.opacity = '1';
                chatWindow.style.visibility = 'visible';
                chatWindow.style.pointerEvents = 'all';
                chatWindow.style.transform = 'scale(1) translateY(0)';
                chatWindow.style.display = 'flex';
            }
            
            // Ensure container is always visible
            const container = document.getElementById('chatbot-container');
            if (container) {
                if (container.style.display === 'none' || !container.style.display) {
                    container.style.display = 'block';
                }
                if (container.style.visibility === 'hidden') {
                    container.style.visibility = 'visible';
                }
            }
        }, 500);
        
        // Mutation Observer - watches for class/style changes
        mutationObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && isChatOpen) {
                    const target = mutation.target;
                    
                    // If someone tries to remove active class while chat is open
                    if (target === chatWindow && mutation.attributeName === 'class') {
                        if (!chatWindow.classList.contains('active')) {
                            console.warn('⚠️ Mutation detected: active class removed! Restoring...');
                            chatWindow.classList.add('active');
                        }
                    }
                    
                    // If someone tries to hide the container
                    if (target.id === 'chatbot-container' && mutation.attributeName === 'style') {
                        const container = target;
                        if (container.style.display === 'none' || container.style.visibility === 'hidden') {
                            console.warn('⚠️ Mutation detected: container hidden! Restoring...');
                            container.style.display = 'block';
                            container.style.visibility = 'visible';
                        }
                    }
                }
            });
        });
        
        // Start observing
        if (chatWindow) {
            mutationObserver.observe(chatWindow, {
                attributes: true,
                attributeFilter: ['class', 'style']
            });
        }
        
        const container = document.getElementById('chatbot-container');
        if (container) {
            mutationObserver.observe(container, {
                attributes: true,
                attributeFilter: ['style', 'class']
            });
        }
        
        console.log('🛡️ Protection mechanism started');
    } catch (error) {
        console.error('❌ Error starting protection:', error);
    }
}

/**
 * Stop protection mechanism (cleanup)
 */
function stopProtection() {
    try {
        if (protectionInterval) {
            clearInterval(protectionInterval);
            protectionInterval = null;
        }
        if (mutationObserver) {
            mutationObserver.disconnect();
            mutationObserver = null;
        }
        console.log('🛡️ Protection mechanism stopped');
    } catch (error) {
        console.error('❌ Error stopping protection:', error);
    }
}

/**
 * Mobile navigation toggle
 */
const navToggle = document.getElementById('navToggle');
const navMenu = document.querySelector('.nav-menu');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Prevent page unload from losing chat state
window.addEventListener('beforeunload', () => {
    saveChatState(isChatOpen);
});

// Log initialization
console.log('%c🎓 Padmashree College Chatbot', 'color: #1e40af; font-size: 16px; font-weight: bold;');
console.log('%cChatbot widget loaded successfully!', 'color: #10b981;');
console.log('%cAPI URL:', 'color: #6b7280;', CONFIG.API_URL);
console.log('%c🛡️ Anti-disappear protection: ENABLED', 'color: #ef4444; font-weight: bold;');
