import numpy as np

long_bound = [-130, -60]
lat_bound = [20,50]

long_bound = [-97.75364555646956, -97.7405353260485] 
lat_bound = [30.26550738856506, 30.27251166760151]

class UserProbabilities():
    def __init__(self, filename, l, nb_users=False, lat_bound=lat_bound, long_bound=long_bound) -> None:
        self.l = l          #power for the number of points in the grid 
        self.delta = 2**l   #grid of size delta*delta
        self.file = filename    #files with data about all users 
        self.data = None    #array of dim 2: length= nb of data, width = user id + positions
        self.width = 0      #width of grid in coordinates x (latitude)
        self.height = 0     #height of grid in coordinates y (longitude)
        self.Gx = None      #array of dim 1: coordinates x of each point of the grid
        self.Gy = None      #array of dim1: coordinates y of each point of the grid
        self.users_probabilities = None     #array of dim 3: 1rst=each unique user, 2*3= grid of size delta*delta with proba of user to be in eavery particular cell of the grid
        self.lat_bound = lat_bound
        self.long_bound = long_bound
        self.n = nb_users

        self.extract_dataset()
        self.create_grid()
        self.get_user_distribution()

    def extract_dataset(self):
        data, user_list = [], []
        with open(self.file, 'r') as file:
            lines = file.readlines()
            if not self.n :
                self.n = len(lines)
            for line in lines:
                column = line.split()
                id_user = int(column[0])
                lat = float(column[2])
                long = float(column[3])
                if self.lat_bound[0] <= lat and lat <= self.lat_bound[1] and self.long_bound[0] <= long and long <= self.long_bound[1] and len(user_list) <= self.n :
                    data.append([id_user, long, lat])
                    if not id_user in user_list:
                        user_list.append(id_user)
        
        self.data = np.array(data)

    def create_grid(self):
        widths = self.data[:,1]
        heights = self.data[:,2]
        self.width = np.max(widths) - np.min(widths)
        self.height = np.max(heights) - np.min(heights)
        self.width_delta = self.width / self.delta
        self.height_delta = self.height / self.delta
        self.Gx = np.arange(np.min(widths), np.min(widths)+self.width, self.width_delta)
        self.Gy = np.arange(np.min(heights), np.min(heights)+self.height, self.height_delta)

    def get_user_distribution(self):
        user_ids = np.unique(self.data[:,0])
        self.users_probabilities = []
        for i, user_id in enumerate(user_ids):
            user_grid = np.zeros((self.delta, self.delta))
            user_data = self.data[self.data[:,0] == user_id][:,1:3]
            for coord in user_data :
                x,y = coord[0], coord[1]
                i = np.searchsorted(self.Gx, x, 'right') -1
                j = np.searchsorted(self.Gy, y, 'right') -1
                user_grid[i,j] += 1
            user_grid /= len(user_data)

            self.users_probabilities.append(user_grid) #.reshape(-1)
        self.users_probabilities = np.array(self.users_probabilities)

class PreProcessing(UserProbabilities):
    def __init__(self, filename, l, nb_users) -> None:
        # super().__init__(filename, 12, nb_users)
        # long, lat = self.get_most_lived_area()
        # print("long, lat", long, lat)
        super().__init__(filename, l, nb_users)

    def get_most_lived_area(self):
        total_dist = np.sum(self.users_probabilities, axis=0)
        most_lived_area = np.unravel_index(np.argmax(total_dist), total_dist.shape)
        long_range = [self.Gx[most_lived_area[0]], self.Gx[most_lived_area[0]]+ self.width_delta]
        lat_range = [self.Gy[most_lived_area[1]], self.Gy[most_lived_area[1]]+ self.height_delta]
        return long_range, lat_range

                
def main():
    #user = UserProbabilities('test.txt', l=2)
    #area = PreProcessing('dataset720.txt', l=2)
    None

    
if __name__ == "__main__":
    main()