# -*- coding: utf-8 -*-
"""Model Klasifikasi Gambar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z8KZb4LPq4DqxUpZtZrZc5KT0VSqcGjp

Mencek Version
"""



import tensorflow as tf
print(tf.__version__)

"""Install Gdown"""

!pip install gdown

"""Unduh File menggunakan gdown"""

!gdown --id 1ZKnT0F95tRNnjo57qMixfACoFy3ITEj7 -O /tmp/messy_vs_clean_room.zip

"""Ekstraksi pada file zip"""

# melakukan ekstraksi pada file zip
import zipfile,os
local_zip = '/tmp/messy_vs_clean_room.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

base_dir = '/tmp/images'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')

os.listdir('/tmp/images/train')

os.listdir('/tmp/images/val')

"""Kode berikut menunjukkan proses augmentasi gambar pada setiap sampel di dataset."""

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
                rescale=1./255,
                rotation_range=20,
                horizontal_flip=True,
                shear_range = 0.2,
                fill_mode = 'nearest')
test_datagen = ImageDataGenerator(
                    rescale=1./255)

"""siapkan data latih dan validasi dari kumpulan data gambar yang di-load dalam
memori melalui fungsi flow() berikut.
"""

train_generator = train_datagen.flow_from_directory(
    train_dir,  # direktori data latih
    target_size=(150, 150),  # mengubah resolusi seluruh gambar menjadi 150x150 piksel
    batch_size=4,
    class_mode='binary'  # karena ini merupakan masalah klasifikasi 2 kelas
)

validation_generator = test_datagen.flow_from_directory(
    validation_dir,  # direktori data validasi
    target_size=(150, 150),  # mengubah resolusi seluruh gambar menjadi 150x150 piksel
    batch_size=4,  # karena ini merupakan masalah klasifikasi 2 kelas
    class_mode='binary'
)

"""layer max pooling berguna untuk mereduksi resolusi gambar
sehingga proses pelatihan model lebih cepat. Nah, pada model CNN, proses klasifikasi
gambar hanya berfokus pada atribut-atribut unik yang membedakan tiap kategori. Sehingga,
teknik ini dinilai lebih optimal dibandingkan hanya menggunakan model MLP yang
membedakan tiap kategori dengan melihat keseluruhan piksel-piksel pada gambar.
"""

model = tf.keras.models.Sequential([
tf.keras.layers.Conv2D(32, (3,3), activation='relu',
input_shape=(150, 150, 3)),
tf.keras.layers.MaxPooling2D(2, 2),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Conv2D(512, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),])
model = tf.keras.models.Sequential([
tf.keras.layers.Conv2D(32, (3,3), activation='relu',
input_shape=(150, 150, 3)),
tf.keras.layers.MaxPooling2D(2, 2),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Conv2D(512, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(512, activation='relu'),
tf.keras.layers.Dense(1, activation='sigmoid')])

model.summary()

# compile model dengan 'adam' optimizer loss function
'binary_crossentropy'
model.compile(loss='binary_crossentropy',

optimizer=tf.optimizers.Adam(),

metrics=['accuracy'])

# latih model dengan model.fit
model.fit(

train_generator,
steps_per_epoch=25,  # berapa batch yang akan dieksekusi pada setiap epoch
epochs=20, # tambahkan epochs jika akurasi model belum optimal
validation_data=validation_generator, # menampilkan akurasi pengujian data validasi
validation_steps=5,  # berapa batch yang akan dieksekusi pada setiap epoch
verbose=2)

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

uploaded = files.upload()
for fn in uploaded.keys():
# predicting images
  path = fn
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)
  print(fn)
  if classes==0:
    print('clean')
  else:
   print('messy')
