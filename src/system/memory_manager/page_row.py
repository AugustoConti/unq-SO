class PageRow:
    def __init__(self, frame=-1, swap=-1, load_time=-1, last_access_time=-1, sc=0):
        self.frame = frame
        self.swap = swap
        # loadTime - tick en que se cargo en memoria en pagefault(para fifo)
        self.loadTime = load_time
        # lastAccessTime - update en mmu cada vez que se accede a esa pagina (LRU, saca el nro menor, el mas viejo)
        self.lastAccessTime = last_access_time
        # SC - cada vez que mmu accede, pone en 1, se crea en 0 (Second chance)
        self.SC = sc

    def __repr__(self):
        return "PageRow( Frame: {f}, Swap: {s}, LoadTime: {lt}, LastAccess: {la}, SC: {sc} )" \
            .format(f=self.frame, s=self.swap, lt=self.loadTime, la=self.lastAccessTime, sc=self.SC)
