import pandas as pd
import numpy as np

def UploadGuestlist():

    guestlist = pd.read_csv("../../data/test_guestlist.csv", sep = ";")
    dim = len(guestlist)

    guestlist["closeness"] = guestlist.apply(lambda x: " ".join(x[["Bride/Groom", "Cluster"]]), axis=1)
    guestlist["full name"] = guestlist.apply(lambda x: " ".join(x[[0, 1]]), axis=1)

    # variants how a plus one can be entered without giving a name
    plusone = ["+1", "+ 1", "plus one"]

    i = 0

    for i in range(0, dim):
        if guestlist.loc[i, "attending w/"] in plusone:
            guestlist.loc[dim] = ["+1 of ", guestlist.loc[i, "full name"], np.nan, np.nan, guestlist.loc[i, "full name"], np.nan , "+1 of " + guestlist.loc[i, "full name"]]
            guestlist.loc[i, "attending w/"] = "+1 of " + guestlist.loc[i, "full name"]
            dim += 1

def CreateRelationships():
    # Dictionary for relationship values
    weight = {"bride family":500, "groom family":500, "partner":2000, "bride friends":300, "groom friends":300}
    # create array with size len(guestlist) x len(guestlist) filled w/ 0s to initialise DF
    guest_df = pd.DataFrame(np.random.randint(low=0, high=1, size=(dim, dim)))

    i = 0
    # go through all rows
    for i in range(0, dim):

        # look up cluster ID (equals entry in column "closeness" of that row)
        clusterID = guestlist.loc[i, "closeness"]
        partnerID = guestlist.loc[i, "attending w/"]

        # return an array with all row indices with the same clusterID
        congruent = np.array(np.where(guestlist["closeness"] == clusterID))
        partner = np.where(guestlist["full name"] == partnerID)

        # write values into guest_df: for each row write weight for clusterID
        # if i == j don't overwrite 0
        j = 0
        for j in range (0, dim):
            if j in congruent and i != j:
                guest_df.loc[i,j] += weight[clusterID]

            if j in partner:
                guest_df.loc[i,j] += weight["partner"]

#    print(guest_df)

def BetterThanRandom():
# initial values for number of people, seats per table, iterations
attending = dim
seats_per_table = 5
iters = 20
tablenumber = 1

# transform guest_df into a numpy array -> guest_matrix
guest_matrix = np.array(guest_df)

# create empty data frame to save results
seating = pd.DataFrame()

#print(guest_matrix)


#def seating_iterative(attending, seats_per_table, iters, guest_matrix):

while attending > 0:

    # create binary numpy array with given values
    arr = np.array([1]*seats_per_table + [0]*(attending - seats_per_table) )

    # for testing only
    np.random.shuffle(arr)

    # initialise best fit and best array for comparison
    arr_best = np.array(arr)
    fit_best = guest_matrix.dot(arr_best).dot(arr_best)

    # while loop for seating iteratively
    i = 0
    while i < iters:
        np.random.shuffle(arr)
        fit_new = guest_matrix.dot(arr).dot(arr)

        if fit_new > fit_best:
            arr_best = np.array(arr)
            fit_best = fit_new
    #print statement for testing only
        #print (arr_best, "; ", fit_best, "; ",arr, "; ",fit_new)
        i += 1

    # determine indices of rows to be deleted
    # maybe improve by using the np.where function -> see transformation of input
    get_indexes = lambda arr_best, xs: [j for (y, j) in zip(xs, range(len(xs))) if arr_best == y]
    i_del = get_indexes(1,arr_best)
    #print(i_del)

    # deleting seated guests from guest matrix
    guest_matrix = np.delete(guest_matrix, i_del, 0)
    guest_matrix = np.delete(guest_matrix, i_del, 1)
    #print(guest_matrix)

    table_id = "table " + str(tablenumber)

    #print(table_id)

    y = 0 < arr_best

    names = np.array(guestlist.loc[y, "full name"])

    #print(y)

    #print(guestlist)

    seating[table_id] = names

    guestlist = pd.DataFrame(guestlist.drop(guestlist.index[i_del]))



    #print(seating)

    #seating[table_id] = guestlist.loc(i_del, "fullname")

    # minimise attending
    attending -= seats_per_table
    tablenumber += 1
