import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle
from matplotlib.widgets import Button
import random
import os
import sys
import matplotlib.font_manager as fm

def resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 设置字体
def setup_fonts():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe运行
        try:
            # 尝试加载打包的字体
            font_path = resource_path(os.path.join('fonts', 'SimHei.ttf'))
            if os.path.exists(font_path):
                fm.fontManager.addfont(font_path)
                plt.rcParams['font.sans-serif'] = ['SimHei']
            else:
                # 如果找不到打包的字体，使用系统字体
                plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        except:
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    else:
        # 如果是直接运行python脚本
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    
    plt.rcParams['axes.unicode_minus'] = False

# 在程序开始时调用setup_fonts
setup_fonts()
plt.style.use('dark_background')

class DescalingAnimation:
    def __init__(self):
        # 设置图形和坐标轴
        self.fig, self.ax = plt.subplots(figsize=(12, 5))
        # 调整子图位置，为图例和按钮留出空间
        self.fig.subplots_adjust(bottom=0.2, right=0.85)
        self.fig.patch.set_facecolor('#1a1a1a')  # 设置深灰色背景
        self.ax.set_facecolor('#1a1a1a')
        self.ax.set_xlim(-0.5, 10.5)  # 扩大x轴显示范围
        self.ax.set_ylim(0, 4)
        self.ax.set_aspect('equal')
        
        # 绘制管道 - 使用金属质感的颜色
        pipe_color = '#4a4a4a'
        edge_color = '#6a6a6a'
        self.pipe_top = Rectangle((0, 3), 10, 0.2, color=pipe_color, 
                                ec=edge_color, linewidth=1)
        self.pipe_bottom = Rectangle((0, 1), 10, 0.2, color=pipe_color,
                                   ec=edge_color, linewidth=1)
        self.ax.add_patch(self.pipe_top)
        self.ax.add_patch(self.pipe_bottom)
        
        # 初始化水垢粒子
        self.scale_particles = []
        self.create_scale_particles()
        
        # 初始化除垢剂粒子
        self.descaling_agents = []
        self.create_descaling_agents()
        
        # 设置现代感标题
        plt.title('佰宏除垢灵工作原理', fontsize=16, pad=20, 
                 color='#ffffff', fontweight='bold')
        
        # 隐藏坐标轴
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # 添加网格背景增加科技感
        self.ax.grid(True, linestyle='--', alpha=0.1, color='#ffffff')
        
        # 添加图例
        # 创建图例项
        legend_elements = [
            Circle((0, 0), radius=0.3, color='#00ffff', alpha=0.6, label='除垢灵分子'),
            Circle((0, 0), radius=0.05, color='#cd853f', alpha=0.8, label='外层水垢'),
            Circle((0, 0), radius=0.05, color='#b8860b', alpha=0.8, label='中层水垢'),
            Circle((0, 0), radius=0.05, color='#8b4513', alpha=0.8, label='内层水垢')
        ]
        
        # 添加图例，放在图形右侧
        self.ax.legend(handles=legend_elements, 
                      loc='center left',
                      bbox_to_anchor=(1.02, 0.5),
                      title='图例说明',
                      title_fontsize=12,
                      fontsize=10,
                      frameon=True,
                      facecolor='#2a2a2a',
                      edgecolor='#4a4a4a',
                      labelcolor='white',
                      borderpad=1)
        
        # 添加文字说明
        text_color = '#ffffff'
        self.fig.text(0.02, 0.02, 
                     '动画说明：除垢灵分子随水流方向由左向右流动，打破水垢分子间的范德华力，吸附并带走水垢', 
                     color=text_color, 
                     fontsize=10,
                     ha='left')
        
        
        # 保存动画对象的引用
        self.anim = None
        
    def create_scale_particles(self):
        # 在管道内壁创建多层水垢粒子 - 使用渐变色
        scale_colors = ['#cd853f', '#b8860b', '#8b4513']  # 从浅到深的褐色
        scale_names = ['外层水垢', '中层水垢', '内层水垢']
        
        # 为每层创建更密集的水垢分布
        for layer in range(3):
            # 创建更密集的x坐标点
            x_positions = np.linspace(1, 9, 30)  # 固定间隔的点
            for x_base in x_positions:
                # 在每个基准点周围添加随机偏移的粒子
                for _ in range(4):  # 每个基准点周围4个粒子
                    x = x_base + random.uniform(-0.1, 0.1)
                    
                    # 上下管壁各生成一组粒子
                    for base_y in [2.8 - layer * 0.15, 1.2 + layer * 0.15]:
                        y = base_y + random.uniform(-0.05, 0.05)
                        
                        particle = Circle((x, y), 0.04, color=scale_colors[layer], 
                                        alpha=0.8)
                        self.scale_particles.append({
                            'particle': particle,
                            'attached': True,
                            'layer': layer,
                            'original_pos': (x, y),
                            'name': scale_names[layer],
                            'connections': []  # 存储与相邻粒子的连接
                        })
                        self.ax.add_patch(particle)
        
        # 创建粒子间的范德华力连接
        self.van_der_waals = []
        for i, scale1 in enumerate(self.scale_particles):
            p1 = scale1['particle']
            for j, scale2 in enumerate(self.scale_particles[i+1:], i+1):
                p2 = scale2['particle']
                if scale1['layer'] == scale2['layer']:  # 只连接同层粒子
                    dx = p1.center[0] - p2.center[0]
                    dy = p1.center[1] - p2.center[1]
                    distance = np.sqrt(dx**2 + dy**2)
                    
                    if distance < 0.15:  # 近邻粒子才建立连接
                        # 创建连接线
                        line = plt.Line2D([p1.center[0], p2.center[0]],
                                        [p1.center[1], p2.center[1]],
                                        color='white', alpha=0.2, linewidth=0.5)
                        self.ax.add_line(line)
                        self.van_der_waals.append({
                            'line': line,
                            'particle1': scale1,
                            'particle2': scale2,
                            'original_distance': distance,
                            'breaking': False,
                            'break_progress': 0
                        })
                        # 记录粒子间的连接
                        scale1['connections'].append(len(self.van_der_waals) - 1)
                        scale2['connections'].append(len(self.van_der_waals) - 1)

    def create_descaling_agents(self):
        # 创建发光效果的除垢剂粒子
        for _ in range(2):
            x = random.uniform(1, 0)
            y = random.uniform(1.5, 2.5)
            # 主粒子
            agent = Circle((x, y), 0.3, color='#00ffff', alpha=0.6)  # 青色
            # 添加光晕效果
            glow = Circle((x, y), 0.4, color='#00ffff', alpha=0.2)
            self.ax.add_patch(glow)
            self.descaling_agents.append({
                'main': agent,
                'glow': glow
            })
            self.ax.add_patch(agent)
    
    def update(self, frame):
        artists = []
        
        # 计算当前清除的层级
        # 每150帧为一个完整循环，总共需要4个循环
        cycle = int(frame / 150)  # 0-3，表示第几遍
        
        # 更新除垢剂粒子位置和光晕效果
        for agent_group in self.descaling_agents:
            # 每次循环结束时重置位置
            if frame % 150 == 0:  # 增加每次循环的帧数
                new_x = -2
                new_y = random.uniform(1.5, 2.5)
                agent_group['main'].center = (new_x, new_y)
                agent_group['glow'].center = (new_x, new_y)
            else:
                new_x = agent_group['main'].center[0] + 0.08
                new_y = agent_group['main'].center[1]
                agent_group['main'].center = (new_x, new_y)
                agent_group['glow'].center = (new_x, new_y)
                
                # 只在到达右边界时重置
                if new_x > 12:  # 延长移动距离
                    new_x = -2
                    new_y = random.uniform(1.5, 2.5)
                    agent_group['main'].center = (new_x, new_y)
                    agent_group['glow'].center = (new_x, new_y)
            
            # 添加脉动效果
            pulse = 0.05 * np.sin(frame * 0.1)
            agent_group['glow'].set_radius(0.4 + pulse)
            
            artists.append(agent_group['main'])
            artists.append(agent_group['glow'])
            
            # 根据循环次数决定要清除的层
            if cycle < 3:  # 前三遍，每次清除一层
                target_layers = [2 - cycle]  # 从内层开始清除
            else:  # 第四遍清除所有剩余的水垢
                target_layers = [0, 1, 2]
            
            # 检测与目标层水垢粒子的碰撞
            for scale in self.scale_particles:
                if scale['attached'] and scale['layer'] in target_layers:
                    dx = new_x - scale['particle'].center[0]
                    dy = new_y - scale['particle'].center[1]
                    distance = np.sqrt(dx**2 + dy**2)
                    
                    if distance < 0.8:
                        scale['attached'] = False
                        angle = random.uniform(0, 2 * np.pi)
                        base_radius = 0.4
                        radius = base_radius + scale['layer'] * 0.1
                        scale['particle'].center = (
                            new_x + radius * np.cos(angle),
                            new_y + radius * np.sin(angle)
                        )
                        scale['agent'] = agent_group['main']
        
        # 移动已经脱离的水垢粒子
        for scale in self.scale_particles:
            if not scale['attached']:
                if 'agent' in scale:
                    angle = random.uniform(0, 2 * np.pi)
                    base_radius = 0.4
                    radius = base_radius + scale['layer'] * 0.1
                    scale['particle'].center = (
                        scale['agent'].center[0] + radius * np.cos(angle),
                        scale['agent'].center[1] + radius * np.sin(angle)
                    )
            artists.append(scale['particle'])
        
        # 重置超出边界的除垢剂和水垢粒子
        for agent_group in self.descaling_agents:
            if agent_group['main'].center[0] > 10:
                new_x = -2
                new_y = random.uniform(1.5, 2.5)
                agent_group['main'].center = (new_x, new_y)
                agent_group['glow'].center = (new_x, new_y)
        
        # 更新范德华力连接线
        for connection in self.van_der_waals:
            p1 = connection['particle1']
            p2 = connection['particle2']
            line = connection['line']
            
            # 更新连接线位置
            line.set_data([p1['particle'].center[0], p2['particle'].center[0]],
                         [p1['particle'].center[1], p2['particle'].center[1]])
            
            # 检查是否需要断开连接
            if not p1['attached'] or not p2['attached']:
                if not connection['breaking']:
                    connection['breaking'] = True
                
            # 处理断裂效果
            if connection['breaking']:
                connection['break_progress'] += 0.1
                # 断裂过程中的透明度变化
                alpha = max(0, 0.2 - connection['break_progress'])
                line.set_alpha(alpha)
                # 添加断裂时的闪光效果
                if 0.2 <= connection['break_progress'] <= 0.4:
                    line.set_color('#ffffff')
                    line.set_linewidth(1.0)
            
            artists.append(line)
        
        return artists

    def restart_animation(self, event):
        # 重置所有粒子位置
        # 重置除垢剂粒子
        for agent_group in self.descaling_agents:
            new_x = random.uniform(-2, 0)
            new_y = random.uniform(1.5, 2.5)
            agent_group['main'].center = (new_x, new_y)
            agent_group['glow'].center = (new_x, new_y)
        
        # 重置水垢粒子
        for scale in self.scale_particles:
            x = random.uniform(1, 9)
            base_y_top = 2.8 - scale['layer'] * 0.1
            base_y_bottom = 1.2 + scale['layer'] * 0.1
            y = random.choice([base_y_top, base_y_bottom])
            scale['particle'].center = (x, y)
            scale['attached'] = True
            if 'agent' in scale:
                del scale['agent']
        
        # 重置范德华力连接
        for connection in self.van_der_waals:
            connection['breaking'] = False
            connection['break_progress'] = 0
            connection['line'].set_alpha(0.2)
            connection['line'].set_color('white')
            connection['line'].set_linewidth(0.5)
        
        # 重新启动动画
        if self.anim is not None:
            self.anim.event_source.stop()
        self.animate()

    def animate(self):
        self.anim = FuncAnimation(
            self.fig, 
            self.update, 
            frames=600,  # 增加总帧数以适应更长的循环
            interval=50,
            blit=True
        )
        plt.show()

if __name__ == "__main__":
    # 设置matplotlib后端
    import matplotlib
    matplotlib.use('TkAgg')  # 使用TkAgg后端，这是一个更稳定的选择
    
    animation = DescalingAnimation()
    animation.animate() 