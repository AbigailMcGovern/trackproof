import napari
import dask.dataframe as dd
import dask.array as da

# proof reading should involve moving the verticies of a track and painting labels using zarpaint


# -------------------
# Data Storage Object
# -------------------


class TrackData:
    def __init__(
        self,
        tracks, 
        image, 
        labels=None, 
        graph=None,
        error_network=None, 
        autofix_network=None
        ):
        '''
        Data storage object for data associated with the proofreading

        Parameters
        ----------
        tracks: pd.DataFrame
            With columns in accordance with napari input
            (ID, t, z, y, x)
        image: array like
            Image data that has been tracked (with dimensions t, z, y, x)
        labels: None or array like
            Segmentation with which tracking was produced (with t, z, y, x)
        graph: dict
            Graph that will describe merging and spliting of tracks with different IDs.
            In accordance with napari API.
        error_network: None or torch.nn.Module subclass
            Network that will produce an error heatmap that will be used to more quickly find errors
        autofix_network: None or torch.nn.Module subclass
            Network that takes error_network output and uses this to correct tracks
        '''
        # set up attributes from the input
        self.original_tracks = dd.DataFrame(tracks)
        if not isinstance(image, da.Array):
            image = da.array(image)
        self.image = image
        if not isinstance(labels, da.Array) and labels is not None:
            labels = da.array(labels)
        self.labels = labels
        self.error_network = error_network
        self.error_map = None
        self.autofix_network = autofix_network
        self.graph = graph

        # private tracks
        self._tracks = tracks
        
        # private corrections 
        self._corrections = {
            'new_vertex' : {}, # key: ID, value: (t, z, y, x)
            'lost_vertex' : {}, # key: ID, value: (t, z, y, x)
            'new_parent' : {}, # key: ID, value: parent ID
            'lost_parent' : {}, # key: ID, value: parent ID
            'join' : {} , # key: ID of first track, value: ID of joined track
            'implemented_corrections' : {
                'new_vertex' : {}, 
                'lost_vertex' : {}, 
                'new_parent' : {}, 
                'lost_parent' : {}, 
                'join' : {}
            }
        }
        self.correction_keys = ['new_vertex', 'lost_vertex', 'new_parent', 'lost_parent', 'join']

        # error rates
        self._errors = {
            'ID swaps' : 0, # +1 when a vertex is moved
            'False terminations' : 0, # +1 when a vertex is added or linked at end
            'True terminations' : 0, # +1 for ever ending that is seen and remains uncorrected
            'False starts' : 0, # +1 when a vertex is added or linked at start
            'True starts' : 0, # +1 for ever start that is seen and remains uncorrected
            'Falsely untracked' : 0, # +1 when vertexes are added to a single particle 'track'
            'Correct': 0 # +1 for every vertex that is observed and seems to be 
                # connected to the correct proceeding vertex
        }
        self.error_keys = ['ID swaps', 'False terminations', 'True terminations', 
                           'False starts', 'True starts', 'Falsely untracked', 'Correct']

    
    @property
    def tracks(self):
        self.update_tracks()
        return self._tracks


    def update_tracks(self):
        # what does one do with the conficts? How do we detect them? 
        pass


    @property
    def corrections(self):
        return self._corrections

    
    @corrections.setter
    def corrections(self, update):
        for key in self.correction_keys:
            self._corrections[key].update(update[key])


    




