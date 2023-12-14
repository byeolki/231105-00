from setting import *

class Setup_Data():
    def __init__(self, guild: Guild) -> None:
        self.path = setup_json_path
        self.guild = guild

    def create_setup(self, channel: TextChannel, message: Message):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        data[str(self.guild.id)] = [channel.id, message.id]
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')

    def del_setup(self):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        del data[str(self.guild.id)]
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')
    
    def check_setup(self) -> bool:
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        return str(self.guild.id) in data
    
    def get_setup(self) -> int:
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        return data[str(self.guild.id)]