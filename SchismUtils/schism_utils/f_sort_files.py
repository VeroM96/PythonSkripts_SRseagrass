#sort schout files 
import glob

def sort_files(ncpat):
   if ncpat[-1] == '/':
       ncpat=ncpat[:-1]
   files = glob.glob(ncpat + '/schout_[0-9].nc')
   files2 = glob.glob(ncpat +'/schout_[0-9][0-9].nc')
   files3 = glob.glob(ncpat +'/schout_[0-9][0-9][0-9].nc')
   files4 = glob.glob(ncpat +'/schout_[0-9][0-9][0-9][0-9].nc')

   def schoutnum(x):
       return(x[len(ncpat)+8:-3])

   files_sorted = sorted(files,key= schoutnum)
   files_sorted.extend(sorted(files2,key=schoutnum))
   files_sorted.extend(sorted(files3,key=schoutnum))
   files_sorted.extend(sorted(files4,key=schoutnum))

   return files_sorted
