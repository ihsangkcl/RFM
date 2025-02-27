import torchvision
import os
import utils.DataTools as dt

aug_train = torchvision.transforms.Compose([
    torchvision.transforms.Resize(256),
    torchvision.transforms.RandomCrop(224),
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(
        [0.5, 0.5, 0.5], [0.25, 0.25, 0.25])
])

aug_test = torchvision.transforms.Compose([
    torchvision.transforms.Resize(256),
    torchvision.transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(
        [0.5, 0.5, 0.5], [0.25, 0.25, 0.25])
])


class selfdataset():
    def getDatasets(self, pathfunc, infolist, transform, process=None, datasetfunc=None):
        datalist = []
        for info in infolist:
            discribe = info[0]
            dirlist = info[1]
            label = info[2]
            cnt = 0
            for dirname in dirlist:
                path = pathfunc(self.folder_path, dirname)
                cnt += len(os.listdir(path))
                datalist.append((path, label))
            print(discribe, cnt)
        if datasetfunc is not None:
            dataset = datasetfunc(datalist, transform=transform, process=process)
        else:
            dataset = dt.imgdataset(datalist, transform=transform, process=process)
        return dataset

    def getsetlist(self, real, setType, process=None, datasetfunc=None):
        setdir = self.R_dir if real is True else self.F_dir
        label = 0 if real is True else 1
        aug = aug_train if setType == 0 else aug_test
        pathfunc = self.trainpath if setType == 0 else self.validpath if setType == 1 else self.testpath
        setlist = []
        for setname in setdir:
            datalist = [(pathfunc(self.folder_path, setname), label)]
            if datasetfunc is not None:
                tmptestset = datasetfunc(datalist, transform=aug, process=process)
            else:
                tmptestset = dt.imgdataset(datalist, transform=aug, process=process)
            setlist.append(tmptestset)
        return setlist, setdir

    def getTrainsetR(self, process=None, datasetfunc=None):
        return self.getDatasets(self.trainpath, [[self.__class__.__name__+" TrainsetR", self.R_dir, 0]], aug_train, process=process, datasetfunc=datasetfunc)

    def getTrainsetF(self, process=None, datasetfunc=None):
        return self.getDatasets(self.trainpath, [[self.__class__.__name__+" TrainsetF", self.F_dir, 1]], aug_train, process=process, datasetfunc=datasetfunc)

    def getTrainset(self, process=None, datasetfunc=None):
        return self.getDatasets(self.trainpath, [[self.__class__.__name__+" TrainsetR", self.R_dir, 0], [self.__class__.__name__+" TrainsetF", self.F_dir, 1]], aug_train, process=process, datasetfunc=datasetfunc)

    def getValidsetR(self, process=None, datasetfunc=None):
        return self.getDatasets(self.validpath, [[self.__class__.__name__+" ValidsetR", self.R_dir, 0]], aug_test, process=process, datasetfunc=datasetfunc)

    def getValidsetF(self, process=None, datasetfunc=None):
        return self.getDatasets(self.validpath, [[self.__class__.__name__+" ValidsetF", self.F_dir, 1]], aug_test, process=process, datasetfunc=datasetfunc)

    def getValidset(self, process=None, datasetfunc=None):
        return self.getDatasets(self.validpath, [[self.__class__.__name__+" ValidsetR", self.R_dir, 0], [self.__class__.__name__+" ValidsetF", self.F_dir, 1]], aug_test, process=process, datasetfunc=datasetfunc)

    def getTestsetR(self, process=None, datasetfunc=None):
        return self.getDatasets(self.testpath, [[self.__class__.__name__+" TestsetR", self.R_dir, 0]], aug_test, process=process, datasetfunc=datasetfunc)

    def getTestsetF(self, process=None, datasetfunc=None):
        return self.getDatasets(self.testpath, [[self.__class__.__name__+" TestsetF", self.F_dir, 1]], aug_test, process=process, datasetfunc=datasetfunc)

    def getTestset(self, process=None, datasetfunc=None):
        return self.getDatasets(self.testpath, [[self.__class__.__name__+" TestsetR", self.R_dir, 0], [self.__class__.__name__+" TestsetF", self.F_dir, 1]], aug_test, process=process, datasetfunc=datasetfunc)


class CelebDF(selfdataset):
    def __init__(self, folder_path="./Celeb-DF"):
        super(selfdataset, self).__init__()
        self.folder_path = folder_path
        self.R_dir = ["Celeb-real", "YouTube-real"]
        self.F_dir = ["Celeb-synthesis"]
        self.trainpath = lambda path, file: os.path.join(self.folder_path, file+"-Img")
        self.validpath = None
        self.testpath = lambda path, file: os.path.join(self.folder_path, file+"-test-Img")


class DFFD(selfdataset):
    def __init__(self, folder_path="./FakeImgDatasets/"):
        super(selfdataset, self).__init__()
        self.folder_path = folder_path
        self.R_dir = ["ffhq"]
        self.F_dir = ["stylegan_ffhq"]
        self.trainpath = lambda path, file: os.path.join(self.folder_path, file, "train")
        self.validpath = lambda path, file: os.path.join(self.folder_path, file, "validation")
        self.testpath = lambda path, file: os.path.join(self.folder_path, file, "test")


class Stylespace(selfdataset):
    def __init__(self, folder_path="./FakeImgDatasets/datasets/"):
        super(selfdataset, self).__init__()
        self.folder_path = folder_path
        self.R_dir = ["real3"]
        self.F_dir = ["(2, 175, -15)", "(2, 175, 15)", "(5, 5, -15)", "(5, 5, 15)","(6, 501, -15)", "(6, 501, 15)", "(8, 17, -15)", "(8, 17, 15)", "(9, 6, -15)", "(9, 6, 15)", "(15, 45, -15)", "(15, 45, 15)", "(12, 84, 15)", "(12, 84, -15)", "(12, 381, -15)", "(12, 381, 15)"]
        #self.F_dir = ["(12, 23, -40)", "(12, 23, -25)", "(12, 23, -10)", "(12, 23, 10)", "(12, 23, 25)", "(12, 23, 40)"]
        #self.F_dir = ["fake"]
        self.trainpath = lambda path, file: os.path.join(self.folder_path, file, "")
        self.validpath = lambda path, file: os.path.join(self.folder_path, file, "")
        self.testpath = lambda path, file: os.path.join(self.folder_path, file, "")
