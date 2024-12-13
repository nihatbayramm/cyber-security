import os
import shutil
import random
import time

class FakeVirusSimulator:
    def __init__(self, target_directory, infection_marker="INFECTED"):
        self.target_directory = target_directory
        self.infection_marker = infection_marker
        self.infected_files = []

    def spread_infection(self):
        print("[*] Enfeksiyon başlatılıyor...")
        for root, _, files in os.walk(self.target_directory):
            for file in files:
                if not file.endswith(".infected"):
                    target_file = os.path.join(root, file)
                    self._infect_file(target_file)

    def _infect_file(self, file_path):
        try:
            with open(file_path, "a") as file:
                file.write(f"\n# {self.infection_marker} - Bu dosya enfekte edilmiştir.\n")
            new_file_path = f"{file_path}.infected"
            shutil.copy(file_path, new_file_path)
            self.infected_files.append(new_file_path)
            print(f"[+] {file_path} -> {new_file_path} (Enfekte edildi)")
        except Exception as e:
            print(f"[!] Dosya enfekte edilemedi: {file_path}, Hata: {e}")

    def create_fake_logs(self):
        log_file = os.path.join(self.target_directory, "system_fake_log.txt")
        print(f"[*] Sahte log oluşturuluyor: {log_file}")
        with open(log_file, "w") as log:
            for _ in range(20):
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                action = random.choice(["Dosya silindi", "Dosya taşındı", "Kopyalama yapıldı", "Yetkisiz erişim"])
                log.write(f"{timestamp} - {action} - {random.randint(1000, 9999)}\n")

    def start(self):
        self.spread_infection()
        self.create_fake_logs()
        print("[*] Enfeksiyon tamamlandı. Eğitim amaçlı virüs çalışması sona erdi.")



if __name__ == "__main__":
    target_dir = input("Hedef dizini girin (örnek: /home/user/Desktop): ").strip()
    if os.path.exists(target_dir):
        virus_sim = FakeVirusSimulator(target_dir)
        virus_sim.start()
    else:
        print("[!] Hedef dizin bulunamadı!")