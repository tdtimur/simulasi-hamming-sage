#############################################
# Import modul tambahan yang akan digunakan #
#############################################

import time

##############################
# Pendefinisian Kode Hamming #
##############################

C = codes.HammingCode(GF(2),4)

###################################
# dict1 = representasi biner data #
# dict2 = Kebalikan dict1         #
###################################

strings = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.'
dict1 = {}
for i in xrange(len(strings)):
    dict1[str(strings[i])] = '{0:011b}'.format(i)

key_dict1 = dict1.keys()
val_dict1 = dict1.values()
    
dict2 = {}
for j in xrange(len(strings)):
    dict2[str(val_dict1[j])] = key_dict1[j]
    
########################################
# Pendefinisian fungsi-fungsi pembantu #
########################################

def str2bin(string):
    return dict1[string]

def bin2vec(biner):
    return vector(GF(2),[int(k) for k in biner])

def vec2bin(vector):
    return ''.join(str(k) for k in vector)

def bin2str(biner):
    return dict2[biner]

def text2bin(t):
    return ''.join(str2bin(j) for j in t)

pretty_print(html("<h2>Kode Hamming (15,11) Teks</h2>"))

##########################################
# Fungsi Interact dan beberapa parameter #
# simulasi yaitu teks, encoder, decoder, #
# dan banyaknya error yang dipilih       #
##########################################

@interact
def _(Teks = 'Saya ingin mencoba menulis pesan dengan menyertakan angka seperti 12345.', Encoder = selector(['Systematic','ParityCheck'], label="Encoder"), Decoder = selector(['NearestNeighbor','Syndrome'], label="Decoder"), Error = (0,2,1), auto_update=False):
    E = Error
    channel = channels.StaticErrorRateChannel(C.ambient_space(),(int(0),int(Error)))
    def entradec_str(string):
        
        ####################################
        # hasil adalah list di mana data   #
        # simulasi disimpan dengan         #
        # hasil[0] encoded, hasil[1]       #
        # transmitted, hasil[2] corrected, #
        # hasil[3] decoded, hasil[4] pesan #
        ####################################
        
        hasil = ['','','','','']
        
        #####################################
        # Proses simulasi per karakter/blok #
        #####################################
        
        for s in string: 
            v = bin2vec(str2bin(s))
            ve = C.encode(v, encoder_name=Encoder)
            ves = vec2bin(ve)
            vt = channel.transmit(ve)
            vts = vec2bin(vt)
            vd = C.decode_to_code(vt, decoder_name=Decoder)
            vds = vec2bin(vd)
            vm = C.decode_to_message(vt, decoder_name=Decoder)
            vms = vec2bin(vm)
            m = bin2str(vms)
            hasil[0] += ves
            hasil[1] += vts
            hasil[2] += vds
            hasil[3] += vms
            hasil[4] += m
        return hasil
        
    ##################
    # Hasil simulasi #
    ##################
    
    start = time.time()
    
    koding = entradec_str(Teks)
    kod0 = koding[0]
    kod1 = koding[1]
    enc1 = bin2vec(kod0)
    tra1 = bin2vec(kod1)
    beda = enc1 + tra1
    count = 0
    for k in xrange(enc1.degree()):
        if enc1[k] != tra1[k]:
            count += 1
    if koding[4] == Teks:
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
    
    pretty_print(html("<h3>Teks Awal:</h3>"))
    print(Teks)
    
    pretty_print(html("<br><h3>Laju Informasi:</h3>"))
    print(C.rate())
    
    pretty_print(html("<h3>Teks Dalam Biner:</h3>"))
    #print(''.join(str2bin(k) for k in Teks))
    print(text2bin(Teks))
    
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
    
    pretty_print(html("<br><h3>Pesan Diterima:</h3>"))
    print(koding[4])
