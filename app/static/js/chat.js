/**
 * Akhil's AI Portfolio Assistant - Client Streaming Chat Script
 * Connects browser UI directly to POST /api/chat/stream Server-Sent Events (SSE).
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatToggleBtn = document.getElementById('chat-widget-toggle');
  const chatModal = document.getElementById('chat-modal');
  const chatCloseBtn = document.getElementById('chat-close-btn');
  const chatClearBtn = document.getElementById('chat-clear-btn');
  const chatForm = document.getElementById('chat-input-form');
  const chatInput = document.getElementById('chat-user-input');
  const chatMessages = document.getElementById('chat-messages');
  const quickPrompts = document.querySelectorAll('.chat-quick-prompt');

  // Conversation Session State
  let conversationId = 'session_' + Math.random().toString(36).substring(2, 9);
  let conversationHistory = [];
  let isStreaming = false;

  const DEFAULT_GREETING_HTML = `
    <div class="chat-msg chat-msg-bot">
      <div class="chat-avatar bot-avatar">
        <i class="fa-solid fa-robot"></i>
      </div>
      <div class="chat-bubble chat-bubble-bot">
        <div class="chat-text-content">
          👋 Hi there! I'm <strong>Akhil's AI Portfolio Assistant</strong>. Ask me anything about Akhil's machine learning projects, skills, tech stack, or experience!
        </div>
      </div>
    </div>
  `;

  // Toggle Chat Modal Open / Close
  function toggleChatModal() {
    if (!chatModal) return;
    const isOpen = chatModal.classList.toggle('active');
    chatToggleBtn.classList.toggle('active', isOpen);
    if (isOpen && chatInput) {
      chatInput.focus();
      scrollToBottom();
    }
  }

  // Clear Chat History & Reset Session State
  function clearChatHistory() {
    if (isStreaming) return;
    conversationHistory = [];
    conversationId = 'session_' + Math.random().toString(36).substring(2, 9);
    if (chatMessages) {
      chatMessages.innerHTML = DEFAULT_GREETING_HTML;
    }
    if (chatInput) {
      chatInput.value = '';
      chatInput.focus();
    }
  }

  if (chatToggleBtn) chatToggleBtn.addEventListener('click', toggleChatModal);
  if (chatCloseBtn) chatCloseBtn.addEventListener('click', toggleChatModal);
  if (chatClearBtn) chatClearBtn.addEventListener('click', clearChatHistory);

  // Quick Starter Prompt Chips
  quickPrompts.forEach(chip => {
    chip.addEventListener('click', () => {
      if (isStreaming) return;
      const promptText = chip.getAttribute('data-prompt') || chip.textContent.trim();
      if (chatInput) chatInput.value = promptText;
      sendMessage(promptText);
    });
  });

  // Handle Form Submission
  if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (isStreaming) return;
      const text = chatInput.value.trim();
      if (!text) return;
      sendMessage(text);
    });
  }

  // Auto-scroll messages container
  function scrollToBottom() {
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }

  // Append a User Message bubble
  function appendUserMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg chat-msg-user';
    msgDiv.innerHTML = `
      <div class="chat-bubble chat-bubble-user">
        <p>${escapeHtml(text)}</p>
      </div>
      <div class="chat-avatar user-avatar">
        <i class="fa-solid fa-user"></i>
      </div>
    `;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  // Create Assistant Message container with typing placeholder
  function createAssistantMessage() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg chat-msg-bot';
    msgDiv.innerHTML = `
      <div class="chat-avatar bot-avatar">
        <i class="fa-solid fa-robot"></i>
      </div>
      <div class="chat-bubble chat-bubble-bot">
        <div class="chat-text-content">
          <span class="chat-typing-dots">
            <span></span><span></span><span></span>
          </span>
        </div>
        <div class="chat-sources-container" style="display: none;"></div>
      </div>
    `;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
    return msgDiv;
  }

  // Send Message & Stream SSE Response
  async function sendMessage(userText) {
    if (!userText || isStreaming) return;

    isStreaming = true;
    if (chatInput) chatInput.value = '';
    if (chatInput) chatInput.disabled = true;

    // 1. Render User Message
    appendUserMessage(userText);
    conversationHistory.push({ role: 'user', content: userText });

    // 2. Render Assistant Message container
    const botMsgDiv = createAssistantMessage();
    const textContentEl = botMsgDiv.querySelector('.chat-text-content');
    const sourcesContainer = botMsgDiv.querySelector('.chat-sources-container');

    let fullAnswerAcc = '';
    let hasReceivedFirstToken = false;

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify({
          query: userText,
          conversation_id: conversationId,
          history: conversationHistory.slice(-10)
        })
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete trailing fragment in buffer

        let currentEvent = 'message';

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i].trim();
          if (!line) continue;

          if (line.startsWith('event:')) {
            currentEvent = line.substring(6).trim();
          } else if (line.startsWith('data:')) {
            const dataStr = line.substring(5).trim();
            try {
              const data = JSON.parse(dataStr);
              handleSSEEvent(currentEvent, data);
            } catch (err) {
              console.warn('[ChatUI] SSE JSON parse note:', err, dataStr);
            }
          }
        }
      }

    } catch (err) {
      console.error('[ChatUI] Stream connection error:', err);
      textContentEl.innerHTML = `<span class="chat-error-text"><i class="fa-solid fa-circle-exclamation"></i> Unable to connect to assistant. Please try again or use the contact form.</span>`;
    } finally {
      isStreaming = false;
      if (chatInput) {
        chatInput.disabled = false;
        chatInput.focus();
      }
      if (fullAnswerAcc) {
        conversationHistory.push({ role: 'assistant', content: fullAnswerAcc });
      }
      scrollToBottom();
    }

    // Process individual SSE Event
    function handleSSEEvent(eventType, data) {
      if (eventType === 'token' && data.token) {
        if (!hasReceivedFirstToken) {
          textContentEl.innerHTML = '';
          hasReceivedFirstToken = true;
        }
        fullAnswerAcc += data.token;
        textContentEl.innerHTML = formatMarkdownText(fullAnswerAcc);
        scrollToBottom();
      } else if (eventType === 'sources' && data.sources && data.sources.length > 0) {
        renderSources(data.sources, data.related_projects || [], sourcesContainer);
      } else if (eventType === 'error') {
        textContentEl.innerHTML = `<span class="chat-error-text"><i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.error || 'Chatbot service error')}</span>`;
      }
    }
  }

  // Render clickable source citations & project pills
  function renderSources(sources, relatedProjects, container) {
    if (!container || !sources.length) return;
    container.style.display = 'block';

    let html = '<div class="chat-sources-header"><i class="fa-solid fa-bookmark"></i> Sources & References</div><div class="chat-sources-list">';

    sources.forEach(src => {
      const linkTag = src.url
        ? `<a href="${src.url}" class="chat-source-chip" target="${src.url.startsWith('http') ? '_blank' : '_self'}">`
        : `<span class="chat-source-chip">`;
      const closeTag = src.url ? '</a>' : '</span>';

      html += `
        ${linkTag}
          <span class="source-num">[${src.citation_id}]</span>
          <span class="source-title">${escapeHtml(src.title)}</span>
          <span class="source-type">${escapeHtml(src.section || src.source_type)}</span>
        ${closeTag}
      `;
    });

    html += '</div>';
    container.innerHTML = html;
    scrollToBottom();
  }

  // Markdown lightweight formatter
  function formatMarkdownText(raw) {
    if (!raw) return '';
    let text = escapeHtml(raw);

    // Bold **text**
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Bullet points * item or - item
    text = text.replace(/^\s*[-*]\s+(.*)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    // Numbered sources [Source 1]
    text = text.replace(/\[Source\s+(\d+)\]/gi, '<span class="chat-inline-citation">[$1]</span>');
    // Line breaks
    text = text.replace(/\n\n/g, '<br><br>');
    text = text.replace(/\n/g, '<br>');

    return text;
  }

  // XSS sanitization helper
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
});
