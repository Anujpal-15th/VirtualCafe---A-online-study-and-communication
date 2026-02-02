/**
 * room.js - Virtual Cafe Room Functionality
 * 
 * This file handles:
 * - WebSocket connection for real-time chat
 * - Join/leave notifications
 * - WebRTC video calling (1-to-1)
 * - Pomodoro timer functionality
 */

// ===== GLOBAL VARIABLES =====

let chatSocket = null;
let peerConnection = null;
let localStream = null;
let remoteStream = null;
let isCallActive = false;
let isMicOn = true;
let isCameraOn = true;

// Timer variables
let timerInterval = null;
let timerMinutes = 25;
let timerSeconds = 0;
let timerRunning = false;

// WebRTC configuration
const rtcConfig = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' }
    ]
};

// ===== WEBSOCKET SETUP =====

/**
 * Initialize WebSocket connection to the room
 * Connects to ws://localhost:8000/ws/rooms/{room_code}/
 */
function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/rooms/${ROOM_CODE}/`;
    
    chatSocket = new WebSocket(wsUrl);
    
    // When connection opens
    chatSocket.onopen = function(e) {
        console.log('WebSocket connected');
        updateVideoStatus('Connected - Ready for video call');
    };
    
    // When message received from server
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        handleWebSocketMessage(data);
    };
    
    // When connection closes
    chatSocket.onclose = function(e) {
        console.log('WebSocket disconnected');
        updateVideoStatus('Disconnected');
        setTimeout(initWebSocket, 3000); // Reconnect after 3 seconds
    };
    
    // On error
    chatSocket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };
}

/**
 * Handle incoming WebSocket messages
 * Routes messages based on type
 */
function handleWebSocketMessage(data) {
    const type = data.type;
    
    switch(type) {
        case 'chat':
            displayChatMessage(data);
            break;
        
        case 'join':
            displayNotification(`${data.username} joined the room`);
            updateMembersList();
            break;
        
        case 'leave':
            displayNotification(`${data.username} left the room`);
            updateMembersList();
            break;
        
        case 'webrtc_offer':
            handleWebRTCOffer(data);
            break;
        
        case 'webrtc_answer':
            handleWebRTCAnswer(data);
            break;
        
        case 'webrtc_ice':
            handleWebRTCICE(data);
            break;
        
        case 'timer':
            handleTimerEvent(data);
            break;
    }
}

// ===== CHAT FUNCTIONALITY =====

/**
 * Display a chat message in the chat box
 */
function displayChatMessage(data) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message';
    
    // Highlight own messages
    if (data.username === USERNAME) {
        messageDiv.classList.add('own');
    }
    
    // Format timestamp
    const timestamp = new Date(data.timestamp).toLocaleTimeString();
    
    messageDiv.innerHTML = `
        <div class="message-username">${data.username}</div>
        <div class="message-text">${escapeHtml(data.message)}</div>
        <div class="message-time">${timestamp}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Display a notification (join/leave) in the chat
 */
function displayNotification(message) {
    const chatMessages = document.getElementById('chat-messages');
    const notifDiv = document.createElement('div');
    notifDiv.className = 'notification-message';
    notifDiv.textContent = message;
    
    chatMessages.appendChild(notifDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Send a chat message through WebSocket
 */
function sendChatMessage(message) {
    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.send(JSON.stringify({
            type: 'chat',
            message: message
        }));
    }
}

/**
 * Update members count (placeholder - in real app would fetch from server)
 */
function updateMembersList() {
    // In a full implementation, you would request updated member list from server
    // For now, just increment/decrement the count displayed
}

/**
 * Escape HTML to prevent XSS attacks
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== WEBRTC VIDEO CALL FUNCTIONALITY =====

/**
 * Start a video call
 * Gets user media (camera + mic) and creates peer connection
 */
async function startCall() {
    try {
        // Get user's camera and microphone
        localStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });
        
        // Display local video
        const localVideo = document.getElementById('local-video');
        localVideo.srcObject = localStream;
        
        // Create peer connection
        peerConnection = new RTCPeerConnection(rtcConfig);
        
        // Add local stream tracks to peer connection
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });
        
        // Handle incoming remote stream
        peerConnection.ontrack = function(event) {
            remoteStream = event.streams[0];
            const remoteVideo = document.getElementById('remote-video');
            remoteVideo.srcObject = remoteStream;
            updateVideoStatus('Connected with peer');
        };
        
        // Handle ICE candidates
        peerConnection.onicecandidate = function(event) {
            if (event.candidate) {
                // Send ICE candidate to other peer via WebSocket
                chatSocket.send(JSON.stringify({
                    type: 'webrtc_ice',
                    candidate: event.candidate
                }));
            }
        };
        
        // Create and send offer
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        
        // Send offer through WebSocket
        chatSocket.send(JSON.stringify({
            type: 'webrtc_offer',
            offer: offer
        }));
        
        isCallActive = true;
        updateCallButtons();
        updateVideoStatus('Calling...');
        
    } catch (error) {
        console.error('Error starting call:', error);
        alert('Could not access camera/microphone. Please check permissions.');
        updateVideoStatus('Error: ' + error.message);
    }
}

/**
 * Handle incoming WebRTC offer from another peer
 */
async function handleWebRTCOffer(data) {
    // Don't handle own offers
    if (data.username === USERNAME) {
        return;
    }
    
    try {
        // Get user media if not already have it
        if (!localStream) {
            localStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            const localVideo = document.getElementById('local-video');
            localVideo.srcObject = localStream;
        }
        
        // Create peer connection if not exists
        if (!peerConnection) {
            peerConnection = new RTCPeerConnection(rtcConfig);
            
            // Add local tracks
            localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, localStream);
            });
            
            // Handle remote stream
            peerConnection.ontrack = function(event) {
                remoteStream = event.streams[0];
                const remoteVideo = document.getElementById('remote-video');
                remoteVideo.srcObject = remoteStream;
                updateVideoStatus('Connected with peer');
            };
            
            // Handle ICE candidates
            peerConnection.onicecandidate = function(event) {
                if (event.candidate) {
                    chatSocket.send(JSON.stringify({
                        type: 'webrtc_ice',
                        candidate: event.candidate
                    }));
                }
            };
        }
        
        // Set remote description (offer)
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
        
        // Create answer
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);
        
        // Send answer back
        chatSocket.send(JSON.stringify({
            type: 'webrtc_answer',
            answer: answer
        }));
        
        isCallActive = true;
        updateCallButtons();
        updateVideoStatus('Call connected');
        
    } catch (error) {
        console.error('Error handling offer:', error);
        updateVideoStatus('Error: ' + error.message);
    }
}

/**
 * Handle incoming WebRTC answer
 */
async function handleWebRTCAnswer(data) {
    // Don't handle own answers
    if (data.username === USERNAME) {
        return;
    }
    
    try {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
        updateVideoStatus('Call connected');
    } catch (error) {
        console.error('Error handling answer:', error);
    }
}

/**
 * Handle incoming ICE candidate
 */
async function handleWebRTCICE(data) {
    // Don't handle own ICE candidates
    if (data.username === USERNAME) {
        return;
    }
    
    try {
        if (peerConnection) {
            await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
        }
    } catch (error) {
        console.error('Error handling ICE candidate:', error);
    }
}

/**
 * End the video call
 */
function endCall() {
    // Stop all local tracks
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
        localStream = null;
    }
    
    // Close peer connection
    if (peerConnection) {
        peerConnection.close();
        peerConnection = null;
    }
    
    // Clear video elements
    document.getElementById('local-video').srcObject = null;
    document.getElementById('remote-video').srcObject = null;
    
    isCallActive = false;
    isMicOn = true;
    isCameraOn = true;
    updateCallButtons();
    updateVideoStatus('Call ended');
}

/**
 * Toggle microphone on/off
 */
function toggleMic() {
    if (localStream) {
        const audioTrack = localStream.getAudioTracks()[0];
        if (audioTrack) {
            audioTrack.enabled = !audioTrack.enabled;
            isMicOn = audioTrack.enabled;
            
            const micBtn = document.getElementById('toggle-mic-btn');
            micBtn.textContent = isMicOn ? '🎤 Mic' : '🎤 Mic (Off)';
            micBtn.style.background = isMicOn ? '' : '#e74c3c';
        }
    }
}

/**
 * Toggle camera on/off
 */
function toggleCamera() {
    if (localStream) {
        const videoTrack = localStream.getVideoTracks()[0];
        if (videoTrack) {
            videoTrack.enabled = !videoTrack.enabled;
            isCameraOn = videoTrack.enabled;
            
            const cameraBtn = document.getElementById('toggle-camera-btn');
            cameraBtn.textContent = isCameraOn ? '📹 Camera' : '📹 Camera (Off)';
            cameraBtn.style.background = isCameraOn ? '' : '#e74c3c';
        }
    }
}

/**
 * Update video status message
 */
function updateVideoStatus(message) {
    const statusEl = document.getElementById('video-status');
    if (statusEl) {
        statusEl.textContent = message;
    }
}

/**
 * Update call button visibility based on call state
 */
function updateCallButtons() {
    const startBtn = document.getElementById('start-call-btn');
    const endBtn = document.getElementById('end-call-btn');
    const micBtn = document.getElementById('toggle-mic-btn');
    const cameraBtn = document.getElementById('toggle-camera-btn');
    
    if (isCallActive) {
        startBtn.style.display = 'none';
        endBtn.style.display = 'inline-block';
        micBtn.style.display = 'inline-block';
        cameraBtn.style.display = 'inline-block';
    } else {
        startBtn.style.display = 'inline-block';
        endBtn.style.display = 'none';
        micBtn.style.display = 'none';
        cameraBtn.style.display = 'none';
    }
}

// ===== POMODORO TIMER FUNCTIONALITY =====

/**
 * Update timer display
 */
function updateTimerDisplay() {
    const display = document.getElementById('timer-display');
    const mins = String(timerMinutes).padStart(2, '0');
    const secs = String(timerSeconds).padStart(2, '0');
    display.textContent = `${mins}:${secs}`;
}

/**
 * Start the Pomodoro timer
 */
function startTimer() {
    if (timerRunning) return;
    
    timerRunning = true;
    updateTimerButtons();
    
    timerInterval = setInterval(() => {
        if (timerSeconds === 0) {
            if (timerMinutes === 0) {
                // Timer complete!
                completeTimer();
                return;
            }
            timerMinutes--;
            timerSeconds = 59;
        } else {
            timerSeconds--;
        }
        updateTimerDisplay();
    }, 1000);
}

/**
 * Pause the timer
 */
function pauseTimer() {
    timerRunning = false;
    clearInterval(timerInterval);
    updateTimerButtons();
}

/**
 * Reset the timer
 */
function resetTimer() {
    pauseTimer();
    timerMinutes = 25;
    timerSeconds = 0;
    updateTimerDisplay();
}

/**
 * Handle timer completion
 * Save study session to database
 */
function completeTimer() {
    pauseTimer();
    
    // Get the original minutes (before countdown)
    const originalMinutes = parseInt(document.getElementById('timer-display').dataset.originalMinutes) || 25;
    
    // Show completion message
    alert(`Congratulations! You completed ${originalMinutes} minutes of focused study!`);
    
    // Save session to database via POST request
    saveStudySession(originalMinutes);
    
    // Reset timer
    resetTimer();
}

/**
 * Save study session to database
 */
function saveStudySession(minutes) {
    // Create form data
    const formData = new FormData();
    formData.append('minutes', minutes);
    formData.append('room_code', ROOM_CODE);
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    // Send POST request
    fetch('/save-session/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken || getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Session saved successfully');
        } else {
            console.error('Failed to save session');
        }
    })
    .catch(error => {
        console.error('Error saving session:', error);
    });
}

/**
 * Get cookie value by name
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Set timer to preset minutes
 */
function setTimerPreset(minutes) {
    pauseTimer();
    timerMinutes = minutes;
    timerSeconds = 0;
    updateTimerDisplay();
    
    // Store original minutes for saving later
    document.getElementById('timer-display').dataset.originalMinutes = minutes;
    
    // Update preset button styling
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.classList.remove('active');
    });
}

/**
 * Update timer button visibility
 */
function updateTimerButtons() {
    const startBtn = document.getElementById('start-timer-btn');
    const pauseBtn = document.getElementById('pause-timer-btn');
    
    if (timerRunning) {
        startBtn.style.display = 'none';
        pauseBtn.style.display = 'inline-block';
    } else {
        startBtn.style.display = 'inline-block';
        pauseBtn.style.display = 'none';
    }
}

/**
 * Handle timer events from other users (optional)
 */
function handleTimerEvent(data) {
    // You can implement synchronized timer across users if needed
    console.log('Timer event from', data.username, ':', data.action);
}

// ===== EVENT LISTENERS =====

document.addEventListener('DOMContentLoaded', function() {
    // Initialize WebSocket
    initWebSocket();
    
    // Chat form submission
    const chatForm = document.getElementById('chat-form');
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (message) {
            sendChatMessage(message);
            input.value = '';
        }
    });
    
    // Video call buttons
    document.getElementById('start-call-btn').addEventListener('click', startCall);
    document.getElementById('end-call-btn').addEventListener('click', endCall);
    document.getElementById('toggle-mic-btn').addEventListener('click', toggleMic);
    document.getElementById('toggle-camera-btn').addEventListener('click', toggleCamera);
    
    // Timer buttons
    document.getElementById('start-timer-btn').addEventListener('click', startTimer);
    document.getElementById('pause-timer-btn').addEventListener('click', pauseTimer);
    document.getElementById('reset-timer-btn').addEventListener('click', resetTimer);
    
    // Timer presets
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const minutes = parseInt(this.dataset.minutes);
            setTimerPreset(minutes);
            this.classList.add('active');
        });
    });
    
    // Custom minutes input
    const customInput = document.getElementById('custom-minutes');
    customInput.addEventListener('change', function() {
        const minutes = parseInt(this.value);
        if (minutes > 0 && minutes <= 120) {
            setTimerPreset(minutes);
        }
    });
    
    // Initialize timer display
    updateTimerDisplay();
    document.getElementById('timer-display').dataset.originalMinutes = 25;
});

// Clean up on page unload
window.addEventListener('beforeunload', function() {
    if (chatSocket) {
        chatSocket.close();
    }
    if (isCallActive) {
        endCall();
    }
});
