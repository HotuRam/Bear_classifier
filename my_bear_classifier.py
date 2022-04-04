# -*- coding: utf-8 -*-
"""my_bear_classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TIeRX2Uz28FhUfypqiFnNRpDLTggRvmS
"""

!pip install -Uqq fastbook
import fastbook
fastbook.setup_book()

from fastbook import *

from google.colab import drive
drive.mount('/content/drive')

bear_types = 'grizzly','black','teddy','panda','polar'

path = Path('/content/drive/MyDrive/bears') #make sure you gave currect path

bears = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(128))

dls = bears.dataloaders(path)

dls.valid.show_batch(max_n=4, nrows=1)

bears = bears.new(item_tfms=Resize(128, ResizeMethod.Squish))
dls = bears.dataloaders(path)
dls.valid.show_batch(max_n=4, nrows=1)

bears = bears.new(item_tfms=RandomResizedCrop(128, min_scale=0.3))
dls = bears.dataloaders(path,bs=5)
dls.train.show_batch(max_n=4, nrows=1, unique=True)

"""### The batch size is by default bs = 64. If you change that value for a lower one, it will work.

## dls = bears.dataloaders(path,bs=5)

"""

bears = bears.new(item_tfms=Resize(128), batch_tfms=aug_transforms(mult=2))
dls = bears.dataloaders(path,bs=64)
dls.train.show_batch(max_n=8, nrows=2, unique=True)

bears = bears.new(
    item_tfms=RandomResizedCrop(224, min_scale=0.5),
    batch_tfms=aug_transforms())
dls = bears.dataloaders(path)

learn = cnn_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(4)

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

interp.plot_top_losses(5, nrows=1)

from fastai.vision.widgets import *

#hide_output
cleaner = ImageClassifierCleaner(learn)
cleaner

for idx in cleaner.delete(): cleaner.fns[idx].unlink()

for idx,cat in cleaner.change(): shutil.move(str(cleaner.fns[idx]), path/cat)

learn.export()

path = Path()
path.ls(file_exts='.pkl')

learn_inf = load_learner(path/'export.pkl')

learn_inf.predict('/content/drive/MyDrive/bears/polar/polar_bear1.jpg')

learn_inf.dls.vocab

"""## Creating a Notebook App from the Model

"""

#hide_output
btn_upload = widgets.FileUpload()
btn_upload

#hide
# For the book, we can't actually click an upload button, so we fake it
btn_upload = SimpleNamespace(data = ['/content/drive/MyDrive/bears/grizzly/grizzly25.jpg'])

img = PILImage.create(btn_upload.data[-1])

# hide_output
out_pl = widgets.Output()
out_pl.clear_output()
with out_pl: display(img.to_thumb(128,128))
out_pl

pred,pred_idx,probs = learn_inf.predict(img)

#hide_output
lbl_pred = widgets.Label()
lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
lbl_pred

btn_run = widgets.Button(description='Classify')
btn_run

def on_click_classify(change):
 img = PILImage.create(btn_upload.data[-1])
 out_pl.clear_output()
 with out_pl: display(img.to_thumb(128,128))
 pred,pred_idx,probs = learn_inf.predict(img)
 lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
btn_run.on_click(on_click_classify)

#hide_output
btn_upload = widgets.FileUpload()
btn_upload

VBox([widgets.Label('Select your bear!'),
      btn_upload, btn_run, out_pl, lbl_pred])

