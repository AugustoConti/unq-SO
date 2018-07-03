class PageRow:
    def __init__(self, frame=-1, swap=-1, load_time=-1, last_access_time=-1, sc=0):
        """
        :type load_time: tick en que se cargo en memoria durante pagefault (fifo)
        :type last_access_time: update en mmu cuando se accede a esa pagina (LRU, saca el nro menor, el mas viejo)
        :type sc: cada vez que mmu accede se pone en 1, se crea en 0 (Second chance)
        """
        self.frame = frame
        self.swap = swap
        self.loadTime = load_time
        self.lastAccessTime = last_access_time
        self.SC = sc

    def to_dict(self):
        return {'frame': self.frame,
                'swap': self.swap,
                'loadTime': self.loadTime,
                'lastAccess': self.lastAccessTime,
                'SC': self.SC}

    def __repr__(self):
        detalle = ','.join(['{k}: {v}'.format(k=k, v=v) for k, v in self.to_dict().items()])
        return "PageRow( {info} )".format(info=detalle)
