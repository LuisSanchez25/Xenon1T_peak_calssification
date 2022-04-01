{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "1b1ad649-1f1e-4bc7-8091-7675be7dafdd",
   "metadata": {},
   "outputs": [],
   "source": [
    "import strax\n",
    "import straxen\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d3138692-7ffb-43ab-85e2-b00df1ab9b58",
   "metadata": {},
   "source": [
    "This notebook will serve to test functions that will be used in the future to create SOM clusters.\n",
    "The main assets that need to be developed will be a recall of the data set as well as a way of applying\n",
    "the clusters we get into neuroscope to the newly recalled data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "1db385c3-6f3a-4f41-b65d-7ffef73da113",
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_cls_acc_v_energy(data, truth, prediction):\n",
    "    '''Function made to create a graph showing how the classification accuracy\n",
    "    varies as a function of area'''\n",
    "    [a , b] = np.histogram(data['area'], bins = 10)\n",
    "    c = (np.digitize(data['area'],b))\n",
    "    store_bins = np.unique(c)\n",
    "    store_results = np.zeros(np.size(store_bins))\n",
    "    for i in np.arange(np.size(store_bins))+1:\n",
    "        store_results[i-1] = check_accuracy(prediction['type'][np.argwhere(c == i)]+1,\n",
    "                                          truth['type'][np.argwhere(c == i)])\n",
    "    plt.plot(store_results,'x')\n",
    "    \n",
    "    return a"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "488219a6-ff15-477f-835b-00c5568760ed",
   "metadata": {},
   "outputs": [],
   "source": [
    "def compute_win_frequency(weight_cube, data_set):\n",
    "    [A,B,C] = np.shape(weight_cube)\n",
    "    data_size = np.size(data_set, axis=0)\n",
    "    win_freq = np.zeros((A,B))\n",
    "    for i in np.arange(data_size):\n",
    "        loc = np.argwhere(np.sum(weight_cube-data_set[i,:], axis = 2) == np.min(np.sum(weight_cube-data_set[i,:], axis = 2)))\n",
    "        win_freq[loc[0,0],loc[0,1]] = win_freq[loc[0,0],loc[0,1]] + 1\n",
    "        \n",
    "    return win_freq"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "7e5b776a-f077-4433-9261-d626e3aa3f24",
   "metadata": {},
   "outputs": [],
   "source": [
    "def upsample_data(wfdata, max_dt):\n",
    "    '''this function takes in waveforms of different dts and upsamples them by repeating\n",
    "    the elements by the dt value and padding with zeros when necessary\n",
    "    Max dt is just the largest dt to use'''\n",
    "    wfdata = wfdata[wfdata['dt']<=max_dt]\n",
    "    data = wfdata['data'].copy()\n",
    "    dt = wfdata['dt'].copy() // 10 # Integer divide by 10 ns\n",
    "    #max_dt = 8 # units of 10 ns\n",
    "    assert dt.max() <= max_dt\n",
    "\n",
    "    # This will be where the padded waveforms go\n",
    "    S2_padded_data = np.zeros((data.shape[0],\n",
    "                            data.shape[1]*max_dt //10))\n",
    "\n",
    "    for value in np.unique(dt): \n",
    "        # Just pick waveforms with dt of some value, where this is the mask\n",
    "        selection = dt == value\n",
    "\n",
    "    # Fill required values in the padded data\n",
    "        S2_padded_data[selection, 0:value*200] = np.repeat(data[selection],\n",
    "                                                        value,\n",
    "                                                        axis=1,)\n",
    "    return S2_padded_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "678903de-b2fe-40f9-ab35-c48fce2e3efe",
   "metadata": {},
   "outputs": [],
   "source": [
    "def upsample_data_v2(wfdata, max_dt):\n",
    "    '''this function takes in waveforms of different dts and upsamples them by repeating\n",
    "    the elements by the dt value and padding with zeros when necessary\n",
    "    Max dt is just the largest dt to use'''\n",
    "    wfdata = wfdata[wfdata['dt']<=max_dt]\n",
    "    wfdata2 = wfdata[wfdata['dt']>max_dt]\n",
    "    data = wfdata['data'].copy()\n",
    "    \n",
    "    dt = wfdata['dt'].copy() // 10 # Integer divide by 10 ns\n",
    "    dt2 = np.repeat(mat_dt // 10, np.size(wfdata2['dt']))\n",
    "    #max_dt = 8 # units of 10 ns\n",
    "    #assert dt.max() <= max_dt\n",
    "\n",
    "    # This will be where the padded waveforms go\n",
    "    S2_padded_data = np.zeros((wfdata.shape[0],\n",
    "                            wfdata.shape[1]*max_dt))\n",
    "    S2_pd_2 = np.zeros((wfdata2.shape[0],\n",
    "                            wfdata2.shape[1]*max_dt))\n",
    "    for value in np.unique(dt): \n",
    "        # Just pick waveforms with dt of some value, where this is the mask\n",
    "        selection = dt == value\n",
    "        \n",
    "    for value2 in np.unique(dt2): \n",
    "        # Just pick waveforms with dt of some value, where this is the mask\n",
    "        selection2 = dt2 == value2\n",
    "\n",
    "    # Fill required values in the padded data\n",
    "        S2_pd_2[selection2, 0:value2*200] = np.repeat(S2_pd_2,\n",
    "                                                        value,\n",
    "                                                        axis=1,)\n",
    "    Padded_data = np.concatenate((S2_padded_data,S2_pd_2))\n",
    "    Padded_data = np.array(Padded_data)\n",
    "    return S2_padded_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "7a654d09-0e4f-46e4-9e98-efd73ac40186",
   "metadata": {},
   "outputs": [],
   "source": [
    "def recombine_data(s2,s1,s0 = [],num_0_vec = 0):\n",
    "    'recombines data separated by their classes, usually s1 and s2 but occasionally unknown, also has an optional 0vector padding'\n",
    "    [A,B] = np.shape(s2)\n",
    "    s2s1 = np.concatenate((s2,s1))\n",
    "    s2s1s0 = np.concatenate((s2s1,s0))\n",
    "    data = np.concatenate((kr83exp_L1_norm_8000pe,np.zeros((num_0_vec,B))))\n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "54071c9a-72a0-4cf3-b726-bb25f3ddc59d",
   "metadata": {},
   "outputs": [],
   "source": [
    "def export_data(data, export_name):\n",
    "    data_vec = np.reshape(data, (len(data[1,:])*len(data[:,1])))\n",
    "    \n",
    "    import struct\n",
    "\n",
    "    f=open(export_name,\"wb\")\n",
    "    export_TL = data_vec\n",
    "    export_TL.dtype\n",
    "    myfmt='f'*len(export_TL)\n",
    "    #  You can use 'd' for double and < or > to force endinness\n",
    "    bin=struct.pack(myfmt,*export_TL)\n",
    "    f.write(bin)\n",
    "    f.close()\n",
    "    #export name must be a string with the extnesion.raw"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "81cdcc67-088d-4883-b16c-9e2c1c542f4a",
   "metadata": {},
   "outputs": [],
   "source": [
    "def assign_labels(data, ref_img, xdim, ydim, cut_out):\n",
    "    '''This functions takes in the data and classifications based on an image gives the\n",
    "    unique labels as well as the data set bacl with the new classification\n",
    "    PS this version only takes in S1s and S2s and ignores unclassified samples, \n",
    "    another version will be made to deal with the unclassified samples\n",
    "    \n",
    "    data: can be either peaks or peak_basics\n",
    "    ref_img: will be the image extracted from the SOM classification of each data point\n",
    "    xdim: width of the image cube\n",
    "    ydim: height of the image cube\n",
    "    cut_out: removes the n last digits of the image vector if necesarry'''\n",
    "    from PIL import Image\n",
    "    img = Image.open(ref_img)\n",
    "    imgGray = img.convert('L')\n",
    "    #imgGray2.save('/home/luissanchez25/im_kr83_real__30x30_2lbl.0.rmpmap.png')\n",
    "    img_color = np.array(img)\n",
    "    img_color_2d = img_color.reshape((xdim*ydim,3))\n",
    "    label = -1 * np.ones(img_color.shape[:-1])\n",
    "    colorp = np.unique(img_color_2d, axis = 0)\n",
    "    for i, color in enumerate(colorp):  # argwhere\n",
    "        label[np.all((img_color == color), axis = 2)] = i\n",
    "    label_vec = label.reshape((xdim*ydim))\n",
    "    if cut_out != 0:\n",
    "        label_vec_nonzero = label_vec[:-cut_out]\n",
    "    elif cut_out == 0:\n",
    "        label_vec_nonzero = label_vec\n",
    "    s2_data = data[data['type'] == 2]\n",
    "    s1_data = data[data['type'] == 1]\n",
    "    som_class_peaks = np.concatenate((s2_data,s1_data)) #note had to reverse s2,s1 to s1,s2\n",
    "    som_class_peaks['type'] = label_vec_nonzero\n",
    "    \n",
    "    return colorp, som_class_peaks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "91679305-ab06-47e0-a651-e8fabd1f02d2",
   "metadata": {},
   "outputs": [],
   "source": [
    "class_nums = [8761, 8761+8992, 1e10]\n",
    "def generate_incl_file(filename, xcube, ycube, class_nums):\n",
    "    '''generates a file that tells NS what the label of each data point is. this needs:\n",
    "    filename: such as 'data.incl'\n",
    "    xcube: horizontal dimension of the data cube\n",
    "    ycube: vertical dimension of the data cube\n",
    "    class_nums: vector of 3 dimensions detailing where the labels should swtich, the values of each vector should be its own puls the previous'''\n",
    "    f = open(filename, \"w+\")\n",
    "    count = 1\n",
    "    for i in np.arange(ycube):\n",
    "        for j in np.arange(xcube):\n",
    "            if count <= class_nums[0]:\n",
    "                f.write('include area ' \n",
    "                        +str(j+1) + ' ' \n",
    "                        +str(i+1) + ' ' \n",
    "                        +str(j+1) + ' ' \n",
    "                        +str(i+1) + ' C' + ' \\n')\n",
    "            if count > class_nums[0] and count <= class_nums[1]:\n",
    "                f.write('include area ' \n",
    "                        +str(j+1) + ' ' \n",
    "                        +str(i+1) + ' ' \n",
    "                        +str(j+1) + ' ' \n",
    "                        +str(i+1) + ' G' + '\\n')\n",
    "            if count > class_nums[1]:\n",
    "                f.write('include area ' \n",
    "                        +str(j+1) + ' ' \n",
    "                        +str(i+1) + ' ' \n",
    "                        +str(j+1) + ' ' \n",
    "                        +str(i+1) + ' H' + '\\n')\n",
    "            count = count + 1\n",
    "    f.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "c59764c3-d94d-42e7-b625-bcfd14961758",
   "metadata": {},
   "outputs": [],
   "source": [
    "def check_accuracy(results, truth):\n",
    "    '''Given some classification results and the truth labels, returns an accuracy in terms of percentage'''\n",
    "    data_num = np.size(truth)\n",
    "    correct_classification = 0\n",
    "    for num in np.arange(data_num):\n",
    "        if results[num] == truth[num]:\n",
    "            correct_classification += 1\n",
    "    percent_correct = correct_classification/data_num\n",
    "    return percent_correct"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "b28e94e4-ceb1-49b2-bce0-3a4d531558ab",
   "metadata": {},
   "outputs": [],
   "source": [
    "def generate_confusion_mat(predicted,truth,num_cls):\n",
    "    '''Generate confusion matrix based on list of labels and the number of expected classes\n",
    "    predicted == Whatever your algorithm/NN thinks the labels should be\n",
    "    truth == Ground truth of the labels\n",
    "    num_cls == number of expected classes'''\n",
    "    import pandas as pd\n",
    "    import seaborn as sn\n",
    "    import matplotlib.pyplot as plt\n",
    "\n",
    "    data = {'y_Actual':    truth,\n",
    "            'y_Predicted': predicted\n",
    "            }\n",
    "\n",
    "    df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])\n",
    "    #df = pd.DataFrame(data, columns=['y_Predicted','y_Actual'])\n",
    "    confusion_matrix = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Ground truth'], colnames=['Predicted'], margins = True)\n",
    "    #confusion_matrix = pd.crosstab(df['y_Predicted'], df['y_Actual'], rownames=['Ground truth'], colnames=['Predicted'], margins = True)\n",
    "    a = confusion_matrix\n",
    "    aa = np.array(a)\n",
    "    v = aa[:,num_cls]\n",
    "    confusion_matrix = confusion_matrix / v[:,None]\n",
    "\n",
    "    sn.heatmap(confusion_matrix, annot=True)\n",
    "    #plt.savefig('Qual_imgs/kr83_confusion_mat_SOM.png')\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "0766bf56-5947-4c00-8998-ce01fe317436",
   "metadata": {},
   "outputs": [],
   "source": [
    "def L1_norm(data):\n",
    "    #first 0 out all negative values\n",
    "    data['data'] = np.where(data['data']<0, 0, data['data'])\n",
    "    #now L1 normalize\n",
    "    peaks_L1 = np.zeros((np.shape(data['data'])))\n",
    "    for aa in np.arange(len(data['data'][:,1])):\n",
    "        peaks_L1[aa,:] = data['data'][aa,:]/np.sum(data['data'][aa,:])     \n",
    "    #sanity check\n",
    "    if np.min(peaks_L1) != 0:\n",
    "        print(\"error has occured, data minimum is NOT 0\")\n",
    "        \n",
    "    return peaks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "77b896f9-60cd-4091-9c8a-4aeb4867308d",
   "metadata": {},
   "outputs": [],
   "source": [
    "def L1_norm_c(data):\n",
    "    #first 0 out all negative values\n",
    "    data = np.where(data<0, 0, data)\n",
    "    #now L1 normalize\n",
    "    peaks_L1 = np.zeros((np.shape(data)))\n",
    "    for aa in np.arange(len(data[:,1])):\n",
    "        peaks_L1[aa,:] = data[aa,:]/np.sum(data[aa,:])     \n",
    "    #sanity check\n",
    "    if np.min(peaks_L1) != 0:\n",
    "        print(\"error has occured, data minimum is NOT 0\")\n",
    "        \n",
    "    return peaks_L1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "86a61068-ee38-4c4b-ac75-c22985e99a24",
   "metadata": {},
   "outputs": [],
   "source": [
    "def index_of_fraction(peaks, fractions_desired):\n",
    "    \"\"\"Return the (fractional) indices at which the peaks reach\n",
    "    fractions_desired of their area\n",
    "    :param peaks: strax peak(let)s or other data-bearing dtype\n",
    "    :param fractions_desired: array of floats between 0 and 1\n",
    "    :returns: (len(peaks), len(fractions_desired)) array of floats\n",
    "    \"\"\"\n",
    "    results = np.zeros((len(peaks), len(fractions_desired)), dtype=np.float32)\n",
    "\n",
    "    for p_i, p in enumerate(peaks):\n",
    "        if p['area'] <= 0:\n",
    "            continue  # TODO: These occur a lot. Investigate!\n",
    "        compute_index_of_fraction(p, fractions_desired, results[p_i])\n",
    "    return results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "eac690d1-42ca-46f5-bd13-c92a5efd5f12",
   "metadata": {},
   "outputs": [],
   "source": [
    "def compute_index_of_fraction(peak, fractions_desired, result):\n",
    "    \"\"\"Store the (fractional) indices at which peak reaches\n",
    "    fractions_desired of their area in result\n",
    "    :param peak: single strax peak(let) or other data-bearing dtype\n",
    "    :param fractions_desired: array of floats between 0 and 1\n",
    "    :returns: len(fractions_desired) array of floats\n",
    "    \"\"\"\n",
    "    area_tot = peak['area']\n",
    "    fraction_seen = 0\n",
    "    current_fraction_index = 0\n",
    "    needed_fraction = fractions_desired[current_fraction_index]\n",
    "    for i, x in enumerate(peak['data'][:peak['length']]):\n",
    "        # How much of the area is in this sample?\n",
    "        fraction_this_sample = x / area_tot\n",
    "\n",
    "        # Are we passing any desired fractions in this sample?\n",
    "        while fraction_seen + fraction_this_sample >= needed_fraction:\n",
    "\n",
    "            area_needed = area_tot * (needed_fraction - fraction_seen)\n",
    "            if x != 0:\n",
    "                result[current_fraction_index] = i + area_needed / x\n",
    "            else:\n",
    "                result[current_fraction_index] = i\n",
    "\n",
    "            # Advance to the next fraction\n",
    "            current_fraction_index += 1\n",
    "            if current_fraction_index > len(fractions_desired) - 1:\n",
    "                break\n",
    "            needed_fraction = fractions_desired[current_fraction_index]\n",
    "\n",
    "        if current_fraction_index > len(fractions_desired) - 1:\n",
    "            break\n",
    "\n",
    "        # Add this sample's area to the area seen\n",
    "        fraction_seen += fraction_this_sample\n",
    "\n",
    "    if needed_fraction == 1:\n",
    "        # Sometimes floating-point errors prevent the full area\n",
    "        # from being reached before the waveform ends\n",
    "        result[-1] = peak['length']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "fb4f674b-fda5-4ce3-93d8-48202b9f4531",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "from scipy.stats import beta\n",
    "\n",
    "def calculate_confusion_matrix(true_types, classified_types, with_binomial_errors=True):\n",
    "    \"\"\"\n",
    "    Calculates a confusion matrix and optional\n",
    "    binomial errors given the true types\n",
    "    and classified types for a data set.\n",
    "\t\n",
    "\tParameters\n",
    "\t----------\n",
    "\ttrue_types : array of ints, shape (number of entries in data set)\n",
    "    The ground truth type for each entry in data set.\n",
    "    \n",
    "    classified_types : array of ints, shape (number of entries in data set)\n",
    "    The classified type for each entry in data set.\n",
    "    \n",
    "    with_binomial_errors : bool, default is True\n",
    "    If true, calculate binomial errors for each\n",
    "    value in the confusion matrix.\n",
    "    \n",
    "\tReturns\n",
    "\t-------\n",
    "\tconfusion_matrix : array of ints, shape (number of classes, number of classes)\n",
    "    Number of entries in data set of each true \n",
    "    type / classified type.\n",
    "    \n",
    "    confidence_interval : array of floats, shape (number of classes, number of classes, 2) \n",
    "    The binomial proportion confidence interval \n",
    "    for each entry in the confusion matrix.\n",
    "    \n",
    "    \"\"\"\n",
    "    classes = np.unique(true_types)\n",
    "    num_classes = classes.shape[0]\n",
    "    \n",
    "    confusion_matrix = np.zeros((num_classes,num_classes), dtype=int)\n",
    "    for i, t in enumerate(classes):\n",
    "        true_t = true_types == t\n",
    "        \n",
    "        for j, c in enumerate(classes):\n",
    "            class_c = classified_types == c\n",
    "            confusion_matrix[j,i] = np.sum(class_c & true_t)\n",
    "    \n",
    "    if with_binomial_errors:\n",
    "        \n",
    "        confidence_interval = np.zeros((num_classes,num_classes,2))\n",
    "        \n",
    "        for i in range(num_classes):\n",
    "            all_trials = np.sum(confusion_matrix[:,i])\n",
    "            \n",
    "            for j in range(num_classes):\n",
    "                successes = confusion_matrix[j,i]\n",
    "                interval = beta.interval(0.68, successes+0.5, all_trials-successes+0.5, loc=0, scale=all_trials)\n",
    "                \n",
    "                if confusion_matrix[j,i] >= 1:\n",
    "                    confidence_interval[j,i,:] = [interval[1]-confusion_matrix[j,i], confusion_matrix[j,i]-interval[0]]\n",
    "                else:\n",
    "                    confidence_interval[j,i,:] = [interval[1]-confusion_matrix[j,i], 0]\n",
    "        \n",
    "        return confusion_matrix, confidence_interval\n",
    "    \n",
    "    else:\n",
    "        \n",
    "        return confusion_matrix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "757b12fa-abc1-4219-921c-e1410baca830",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:didacts]",
   "language": "python",
   "name": "conda-env-didacts-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
