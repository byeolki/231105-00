from setting import *

class VC_Data():
    def __init__(self) -> None:
        self.path = vc_json_path

    def create_vc(self, channel: VoiceChannel):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        data[str(channel.id)] = []
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')
    
    def add_vc(self, before: VoiceChannel, after: VoiceChannel):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        data[str(before.id)].append(after.id)
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')

    def del_vc(self, channel: VoiceChannel) -> bool:
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        for before, afters in data.items():
            if channel.id in afters and not channel.members:
                data[before].remove(channel.id)
                with open(self.path, "w", encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent='\t')
                return True
        return False

    def check_temp_vc(self, channel: VoiceChannel) -> bool:
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        for before, afters in data.items():
            if channel.id in afters:
                return True
        return False
    
    def get_vc(self):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        return data

    def check_vc(self, channel: VoiceChannel) -> bool:
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        return str(channel.id) in data