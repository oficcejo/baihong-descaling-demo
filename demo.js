class DescalingAnimation {
    constructor() {
        this.canvas = document.getElementById('animationCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        // 初始化参数
        this.descalingAgents = [];
        this.scaleParticles = [];
        this.vanDerWaals = [];
        this.cycle = 0;
        this.frame = 0;
        
        // 调整初始参数
        this.particleSpeed = 4;  // 降低速度
        this.attractRadius = 80; // 吸附范围
        this.initializeParticles();
        this.animate = this.animate.bind(this);
        this.isAnimating = true;
    }

    initializeParticles() {
        // 创建除垢剂粒子
        for (let i = 0; i < 2; i++) {
            this.descalingAgents.push({
                x: Math.random() * 100 - 200,
                y: Math.random() * 100 + 150,
                radius: 30,
                glowRadius: 40,
                attachedParticles: []  // 存储吸附的水垢粒子
            });
        }

        // 创建水垢粒子
        const scaleColors = ['#cd853f', '#b8860b', '#8b4513'];
        for (let layer = 0; layer < 3; layer++) {
            for (let x = 100; x < 900; x += 30) {
                for (let y of [100 + layer * 15, 300 - layer * 15]) {
                    this.scaleParticles.push({
                        x: x + Math.random() * 10 - 5,
                        y: y + Math.random() * 10 - 5,
                        radius: 4,
                        color: scaleColors[layer],
                        layer: layer,
                        attached: true,
                        originalX: x + Math.random() * 10 - 5,
                        originalY: y + Math.random() * 10 - 5,
                        attachedTo: null,
                        angle: 0
                    });
                }
            }
        }
    }

    drawPipe() {
        // 绘制管道
        this.ctx.fillStyle = '#4a4a4a';
        this.ctx.fillRect(0, 80, this.width, 20);
        this.ctx.fillRect(0, 300, this.width, 20);
    }

    drawParticles() {
        // 绘制除垢剂粒子
        this.descalingAgents.forEach(agent => {
            // 绘制光晕
            const pulseSize = Math.sin(this.frame * 0.05) * 5;  // 添加脉动效果
            const gradient = this.ctx.createRadialGradient(
                agent.x, agent.y, 0,
                agent.x, agent.y, agent.glowRadius + pulseSize
            );
            gradient.addColorStop(0, 'rgba(0, 255, 255, 0.3)');
            gradient.addColorStop(1, 'rgba(0, 255, 255, 0)');
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(agent.x, agent.y, agent.glowRadius + pulseSize, 0, Math.PI * 2);
            this.ctx.fill();

            // 绘制主体
            this.ctx.fillStyle = '#00ffff';
            this.ctx.globalAlpha = 0.6;
            this.ctx.beginPath();
            this.ctx.arc(agent.x, agent.y, agent.radius, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.globalAlpha = 1;
        });

        // 绘制水垢粒子
        this.scaleParticles.forEach(particle => {
            if (particle.attached) {
                // 绘制固定的水垢粒子
                this.ctx.fillStyle = particle.color;
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
                this.ctx.fill();
            } else if (particle.attachedTo) {
                // 绘制被吸附的水垢粒子
                this.ctx.fillStyle = particle.color;
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
                this.ctx.fill();
            }
        });
    }

    update() {
        // 更新除垢剂位置
        this.descalingAgents.forEach(agent => {
            agent.x += this.particleSpeed;
            if (agent.x > this.width + 100) {
                agent.x = -200;
                agent.y = Math.random() * 100 + 150;
            }

            // 检测碰撞和吸附
            this.scaleParticles.forEach(particle => {
                if (particle.attached && particle.layer === Math.floor(this.frame / 600) % 3) {
                    const dx = agent.x - particle.x;
                    const dy = agent.y - particle.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < this.attractRadius) {
                        particle.attached = false;
                        particle.attachedTo = agent;
                        particle.angle = Math.atan2(dy, dx) + Math.random() * Math.PI * 2;
                        agent.attachedParticles.push(particle);
                    }
                }
                
                // 更新被吸附粒子的位置
                if (!particle.attached && particle.attachedTo) {
                    particle.angle += 0.05;
                    const radius = 40 + particle.layer * 10;
                    particle.x = particle.attachedTo.x + Math.cos(particle.angle) * radius;
                    particle.y = particle.attachedTo.y + Math.sin(particle.angle) * radius;
                }
            });
        });

        this.frame++;
    }

    animate() {
        if (!this.isAnimating) return;
        
        this.ctx.clearRect(0, 0, this.width, this.height);
        this.drawPipe();
        this.drawParticles();
        this.update();
        
        requestAnimationFrame(this.animate);
    }

    start() {
        this.isAnimating = true;
        this.animate();
    }

    stop() {
        this.isAnimating = false;
    }

    restart() {
        // 重置所有状态
        this.frame = 0;
        this.cycle = 0;
        
        // 清空所有粒子数组
        this.descalingAgents = [];
        this.scaleParticles = [];
        
        // 重新初始化所有粒子
        this.initializeParticles();
        
        // 清空画布
        this.ctx.clearRect(0, 0, this.width, this.height);
        
        // 如果动画已经停止，重新开始
        if (!this.isAnimating) {
            this.isAnimating = true;
            this.animate();
        }
    }
}

// 创建并启动动画
let animation;
window.onload = () => {
    animation = new DescalingAnimation();
    animation.start();
};

function restartAnimation() {
    if (animation) {
        animation.restart();
    }
} 