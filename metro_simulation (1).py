from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt 

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar [hedef_id]

        from collections import deque
        kuyruk = deque ([(baslangic, [baslangic])])
        ziyaret_edilen = set([baslangic])

        while kuyruk:
            mevcut, rota = kuyruk.popleft()

            if mevcut == hedef:
                return rota

            for komsu, _ in mevcut.komsular:
                if komsu not in ziyaret_edilen:
                    ziyaret_edilen.add(komsu)
                    kuyruk.append((komsu, rota + [komsu]))
        return None



    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = {}
        pq = [(0, id(baslangic),baslangic, [baslangic])]

        while pq:
            toplam_sure,_, mevcut, rota = heapq.heappop(pq)

            if mevcut == hedef:
                return(rota,toplam_sure)
            
            if mevcut in ziyaret_edildi and ziyaret_edildi[mevcut] <= toplam_sure:
                continue

            ziyaret_edildi[mevcut] = toplam_sure

            for komsu, sure in mevcut.komsular:
                yeni_sure = toplam_sure + sure
                heapq.heappush(pq, (yeni_sure,id(komsu),komsu, rota + [komsu]))

        return None



    def metro_gorsellestir(self):
        G = nx.Graph()  

        for istasyon in self.istasyonlar.values():
            G.add_node(istasyon.ad)
        
        kenar_renkleri = []
        for istasyon in self.istasyonlar.values():
            for komsu, sure in istasyon.komsular:
                G.add_edge(istasyon.ad, komsu.ad, weight=sure)
                  
                if "Kırmızı" in istasyon.hat:
                    kenar_renkleri.append("red")
                elif "Mavi" in istasyon.hat:
                    kenar_renkleri.append("blue")
                elif "Turuncu" in istasyon.hat:
                    kenar_renkleri.append("orange")
                else:
                    kenar_renkleri.append("gray") 


        aktarma_noktalari = ["Kızılay", "Gar", "Demetevler"]  
        renkler = []
        node_size = []
        

        for node in G.nodes():
            istasyon = next((i for i in self.istasyonlar.values() if i.ad == node), None)
            if istasyon:
                if istasyon.ad in aktarma_noktalari:
                    renkler.append("yellow")  
                    node_size.append(2000)  
                elif "Kırmızı" in istasyon.hat:
                    renkler.append("red")
                    node_size.append(1000)  
                elif "Mavi" in istasyon.hat:
                    renkler.append("blue")
                    node_size.append(1000)
                elif "Turuncu" in istasyon.hat:
                    renkler.append("orange")
                    node_size.append(1000)
                else:
                    renkler.append("gray")
                    node_size.append(1000)


        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(10,5))
        plt.subplots_adjust(bottom=0.25)  

        nx.draw_networkx_edges(G, pos, edge_color=kenar_renkleri, width=2)
        nx.draw_networkx_nodes(G, pos, node_color=renkler, node_size=node_size)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

        plt.title("Metro Ağı Görselleştirme")
    
        textstr = (
            " Aktarma Merkezleri:\n"
            "- Kızılay\n"
            "- Demetevler\n"
            "- Gar\n\n"
            " Hatlar:\n"
            "Kırmızı Hat: Kızılay, Ulus, Demetevler, OSB\n"
            "Mavi Hat: AŞTİ, Kızılay, Sıhhiye, Gar\n"
            "Turuncu Hat: Batıkent, Demetevler, Gar, Keçiören"
        )
        plt.gcf().text(
            0.72, 0.02, textstr,
            fontsize=8,
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.4', alpha=0.9)
        )
        plt.show(block=True)  


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma


    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 



    ### Kendi test senaryolarım
    """

        print("\n Sıhhiye'den OSB'ye:")
        rota = metro.en_az_aktarma_bul("M3", "K4")
        if rota:
            print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

        sonuc = metro.en_hizli_rota_bul("M3", "K4")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))


        print("\n Batıkent'ten Gar'a:")
        rota = metro.en_az_aktarma_bul("T1", "M4")
        if rota:
            print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

        sonuc = metro.en_hizli_rota_bul("T1", "M4")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

"""



    metro.metro_gorsellestir()



