import subprocess
import os

class VideoConverter:
    def __init__(self, input_path):
        self.input_path = input_path
        
    def convert_video(self, output_path, format="mp4"):
        """
        转换视频到指定格式
        
        Args:
            output_path (str): 输出文件路径
            format (str): 目标格式 (默认: mp4)
        """
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"输入文件不存在: {self.input_path}")
            
        try:
            command = [
                'ffmpeg',
                '-i', self.input_path,
                '-c:v', 'libx264',  # 视频编码器
                '-c:a', 'aac',      # 音频编码器
                '-y',               # 覆盖已存在的文件
                output_path
            ]
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"视频转换失败: {stderr.decode()}")
                
            print(f"视频转换成功！输出文件: {output_path}")
            
        except Exception as e:
            print(f"转换过程中出现错误: {str(e)}")
            raise

    def extract_subtitle(self, output_path):
        """
        提取视频中的字幕流（如果存在）
        
        Args:
            output_path (str): 字幕文件输出路径
            
        Returns:
            str: 如果成功提取字幕，返回字幕文件路径；如果没有字幕流，返回None
        """
        try:
            # 首先检查是否存在字幕流
            check_command = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 's',
                '-show_entries', 'stream=index',
                '-of', 'csv=p=0',
                self.input_path
            ]
            
            result = subprocess.run(check_command, capture_output=True, text=True)
            
            if not result.stdout.strip():
                print("视频中没有找到字幕流")
                return None
                
            # 提取字幕流
            command = [
                'ffmpeg',
                '-i', self.input_path,
                '-map', '0:s:0',  # 选择第一个字幕流
                '-y',
                output_path
            ]
            
            process = subprocess.run(command, capture_output=True, text=True)
            
            if process.returncode == 0:
                print(f"字幕提取成功！输出文件: {output_path}")
                return output_path
            else:
                print("字幕提取失败")
                return None
                
        except Exception as e:
            print(f"字幕提取过程中出现错误: {str(e)}")
            return None
            
    def extract_audio(self, output_path):
        """
        提取视频中的音频流
        
        Args:
            output_path (str): 音频文件输出路径
            
        Returns:
            str: 如果成功提取音频，返回音频文件路径；如果失败，返回None
        """
        try:
            command = [
                'ffmpeg',
                '-i', self.input_path,
                '-vn',  # 不处理视频
                '-acodec', 'pcm_s16le',  # 音频编码为WAV
                '-y',
                output_path
            ]
            
            process = subprocess.run(command, capture_output=True, text=True)
            
            if process.returncode == 0:
                print(f"音频提取成功！输出文件: {output_path}")
                return output_path
            else:
                print("音频提取失败")
                return None
                
        except Exception as e:
            print(f"音频提取过程中出现错误: {str(e)}")
            return None

if __name__ == "__main__":
    # 使用示例
    input_video = "input.mp4"
    output_video = "output.mp4"
    
    converter = VideoConverter(input_video)
    converter.convert_video(output_video) 