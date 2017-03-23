#############################################
# Import modul tambahan yang akan digunakan #
#############################################

import cv2 as cv2
import time
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

##############################
# Pendefinisian Kode Hamming #
##############################

C = codes.HammingCode(GF(2),4)

###################################
# dict1 = representasi biner data #
# dict2 = Kebalikan dict1         #
###################################

dict1 = {}
for i in xrange(256):
    dict1[str(i)] = '{0:011b}'.format(i)

key_dict1 = dict1.keys()
val_dict1 = dict1.values()
    
dict2 = {}
for j in xrange(256):
    dict2[str(val_dict1[j])] = key_dict1[j]
    
########################################
# Pendefinisian fungsi-fungsi pembantu #
########################################

def bin2vec(biner):
    return vector(GF(2),[int(k) for k in biner])

def vec2bin(vector):
    return ''.join(str(k) for k in vector)

pretty_print(html("<h2>Kode Hamming (15,11) Gambar</h2>"))

##########################################
# Fungsi Interact dan beberapa parameter #
# simulasi yaitu teks, encoder, decoder, #
# dan banyaknya error yang dipilih       #
##########################################

@interact
def _(Gambar = selector([DATA+'gem2.jpg',DATA+'gem3.jpg',DATA+'lenna.jpg']), Encoder = selector(['Systematic','ParityCheck'], label="Encoder"), Decoder = selector(['NearestNeighbor','Syndrome']), Error = (0,2,1), auto_update=False):
    start = time.time()
    E = Error
    channel = channels.StaticErrorRateChannel(C.ambient_space(),(int(0),int(Error)))
    gambar = cv2.imread(Gambar,0)
    baris = len(gambar[0])
    kolom = len(gambar)
    def entradec_img(image):
        ####################################
        # hasil adalah list di mana data   #
        # simulasi disimpan dengan         #
        # hasil[0] encoded, hasil[1]       #
        # transmitted, hasil[2] corrected, #
        # hasil[3] decoded, hasil[4] pesan #
        ####################################

        hasil = ['','','','',0,'']
        gambar2 = []
        hitung1 = 0
        hitung2 = 0
        cache = {}
        cache2 = {}
        
        ##############################
        # Proses simulasi per piksel #
        ##############################
        
        for x in gambar:
            gambar2.append([])
            for y in x:
                if str(y) in cache:
                    vb = cache[str(y)]
                else:
                    vb = dict1[str(y)] 
                    cache[str(y)] =  dict1[str(y)]  
                v = bin2vec(vb)
                ve = C.encode(v, encoder_name=Encoder)
                ves = vec2bin(ve)
                vt = channel.transmit(ve)
                vts = vec2bin(vt)
                vd = C.decode_to_code(vt, decoder_name=Decoder)
                vds = vec2bin(vd)
                vm = C.decode_to_message(vt, decoder_name=Decoder)
                vms = vec2bin(vm)
                if str(vms) in cache2:
                    m = int(cache2[str(vms)])
                else:
                    m = int(dict2[str(vms)])
                    cache2[str(vms)] = dict2[str(vms)]
                hasil[0] += ves
                hasil[1] += vts
                hasil[2] += vds
                hasil[3] += vms
                gambar2[hitung1].append(m)
                hasil[5] += vb
                hitung2 += 1
            hitung1 += 1
        hasil[4] = np.array(gambar2,dtype=int)
        return hasil
    
    ##################
    # Hasil simulasi #
    ##################
    
    koding = entradec_img(gambar)
    kod0 = koding[0]
    kod1 = koding[1]
    enc1 = bin2vec(kod0)
    tra1 = bin2vec(kod1)
    beda = enc1 + tra1
    count = 0
    for k in xrange(enc1.degree()):
        if enc1[k] != tra1[k]:
            count += 1
    if np.array_equal(koding[4],gambar) == True:
        print "Data Terkirim Sama Dengan Data Diterima\n"
    else: print "Error. Data Tidak Sama."
    
    end = time.time()
    
    ##############################
    # Menampilkan hasil simulasi #
    ##############################
    
    print "Waktu Komputasi:", end - start ,
    print "s"

    pretty_print(html("<br><h3>Kode Linear:</h3>"))
    print(C)
    
    pretty_print(html("<br><h3>Matriks Cek:</h3>"))
    print(C.parity_check_matrix())
    
    pretty_print(html("<br><h3>Matriks Generator:</h3>"))
    print(C.generator_matrix())
    
    pretty_print(html("<br><h3>Jarak Minimum:</h3>"))
    print(C.minimum_distance())
    
    pretty_print(html("<br><h3>Laju Informasi:</h3>"))
    print(C.rate())
    
    show(matrix_plot(1.0-gambar), axes_labels =['Gambar Awal',''])
    
    if len(koding[5]) <= 6000:
        
        pretty_print(html("<h3>Gambar Dalam Biner:</h3>"))
        print(koding[5])
    
        pretty_print(html("<br><h3>Hasil Encode:</h3>"))
        print(koding[0])
    
        pretty_print(html("<br><h3>Hasil Setelah Transmisi:</h3>"))
        print(koding[1])
    
        pretty_print(html("<br><h3>Error Yang Terjadi:</h3>"))
        print(''.join(str(k) for k in beda))
        print "\n"
        print "Banyaknya error:", count
    
        pretty_print(html("<br><h3>Hasil Koreksi:</h3>"))
        print(koding[2])
    
        pretty_print(html("<br><h3>Hasil Decode:</h3>"))
        print(koding[3])
    
        show(matrix_plot(1.0-koding[4], axes_labels =['Gambar Diterima','']))
    
    else:
        print '' > file(DATA+'img_bin.txt','w')
        print '' > file(DATA+'img_encoded.txt','w')
        print '' > file(DATA+'img_transmitted.txt','w')
        print '' > file(DATA+'img_error.txt','w')
        print '' > file(DATA+'img_decoded.txt','w')
        print '' > file(DATA+'img_received.txt','w')
        
        pretty_print(html("<h3>Gambar Dalam Biner:</h3>"))
        img_bin = file(DATA+'img_bin.txt','w')
        img_bin.write(str(koding[5]))
        pretty_print(html('<a href="/home/admin/7/data/img_bin.txt">img_bin.txt</a>'))
    
        pretty_print(html("<br><h3>Hasil Encode:</h3>"))
        img_encoded = file(DATA+'img_encoded.txt','w')
        img_encoded.write(str(koding[0]))
        pretty_print(html('<a href="/home/admin/7/data/img_encoded.txt">img_encoded.txt</a>'))
    
        pretty_print(html("<br><h3>Hasil Setelah Transmisi:</h3>"))
        img_transmitted = file(DATA+'img_transmitted.txt','w')
        img_transmitted.write(str(koding[1]))
        pretty_print(html('<a href="/home/admin/7/data/img_transmitted.txt">img_transmitted.txt</a>'))
    
        pretty_print(html("<br><h3>Error Yang Terjadi (Hamming Distance):</h3>"))
        img_error = file(DATA+'img_error.txt','w')
        img_error.write(str(''.join(str(k) for k in beda)))
        pretty_print(html('<a href="/home/admin/7/data/img_error.txt">img_error.txt</a>'))
        print "Banyaknya error:", count
    
        pretty_print(html("<br><h3>Hasil Koreksi:</h3>"))
        img_decoded = file(DATA+'img_decoded.txt','w')
        img_decoded.write(str(koding[2]))
        pretty_print(html('<a href="/home/admin/7/data/img_decoded.txt">img_decoded.txt</a>'))
    
        pretty_print(html("<br><h3>Hasil Decode:</h3>"))
        img_received = file(DATA+'img_received.txt','w')
        img_received.write(str(koding[3]))
        pretty_print(html('<a href="/home/admin/7/data/img_received.txt">img_received.txt</a>'))
    
        show(matrix_plot(1.0-koding[4], axes_labels =['Gambar Diterima','']))
