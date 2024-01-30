# -*- coding: utf-8 -*-
"""Tetris_SDK_without_grouped_convolutions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YJ-qKgXc07rbSvPQAmePXi20JEXLJqXa

# Tetris SDK

**This notebook illustrates the algorithm proposed in Tetris-SDK and returns the computing cycles for a specific layer**
"""

import math

# definations

# ckecking marginal space
def marginal_optimizable_row(image, kernel, pw_row):
  if (image-pw_row)%(pw_row - kernel +1) != 0:
    return True
  else:
    return False

def marginal_optimizable_col(image, kernel, pw_col):
  if (image-pw_col)%(pw_col - kernel +1) != 0:
    return True
  else:
    return False

# checking the number of parallel windows
def N_parallel_window(image,kernel,pw_row,pw_col):
  return (math.ceil((image-pw_row) /(pw_row - kernel +1)) + 1)* (math.ceil((image-pw_col) /(pw_col - kernel +1)) + 1)

def N_parallel_window_so(image,kernel,pw_row,pw_col):
  return (math.floor((image-pw_row) /(pw_row - kernel +1)) + 1)* (math.floor((image-pw_col) /(pw_col - kernel +1)) + 1)

# cc considering marginal space, and depth

# cc considering marginal space
def tetris_cc(image, kernel, ic, oc, ar, ac, pw_row, pw_col, pw_ic, pw_oc):
  No_conv = (pw_row - kernel + 1) * (pw_col - kernel + 1)
  # print("No. of conv in one original VWSDK PW is", No_conv)

  No_parallel_window = N_parallel_window(image,kernel,pw_row,pw_col)
  print("    No. of PW for the VWSDK is", No_parallel_window * math.ceil(ic / pw_ic))
  print("-"*30)
  print("    Performing Tetris-SDK")
  print("-"*30)

  optimal_N_parallel_window = No_parallel_window
  so_row = 0 #square-optimized
  so_col = 0
  No_cells = pw_row * pw_col #CIM array row occupied
  No_cells_so = No_cells
  ICt = pw_ic

  moX_row = 0 #marginal_space_window_x_direction
  moX_col = 0

  moY_row = 0
  moY_col = 0

  marginal_space_row = 0
  marginal_space_col = 0

  No_of_moX = 0
  No_of_moY = 0
  found_so = False
  ICmX = 0
  ICmY = 0

  No_windows = 0
  No_windows_so = 0
  No_remaining_parallel_window = No_parallel_window

  do_row = 0 #depth-wise optimized
  do_col = 0
  No_cells_do = No_cells
  mICt = 0

  mmoX_row = 0 #depth-wise marginal
  mmoX_col = 0

  mmoY_row = 0
  mmoY_col = 0

  mmarginal_space_row = 0
  mmarginal_space_col = 0

  No_of_mmoX = 0
  No_of_mmoY = 0

  mICmX = 0
  mICmY = 0


  for i in range(1, int(pow(No_conv, 1 / 2))+1):
        if No_conv % i == 0 and found_so == False:
          # print("FACTOR: " + str(i) +"*"+str(int(No_conv / i)))
          sw_row = i + kernel -1
          sw_col = int(No_conv / i) + kernel -1
          # print("sw_pw is", sw_row, "*", sw_col)
          # print("cc is", N_parallel_window(image,kernel,sw_row,sw_col))
          # print(N_parallel_window(image,kernel,sw_row,sw_col))
          # print(ptimal_N_parallel_window)
          if (N_parallel_window(image,kernel,sw_row,sw_col)<= optimal_N_parallel_window) and (sw_row*sw_col < No_cells) :
            optimal_N_parallel_window = N_parallel_window(image,kernel,sw_row,sw_col)
            so_row = sw_row
            so_col = sw_col
            No_cells_so = sw_row*sw_col
            ICt = ar // No_cells_so
            found_so = True
            # print("!!!!!found_so", found_so)
            # print(so_row, "x", so_col, "square-inclined window is better than the original PW", pw_row, pw_col)
            print("Square-inclined window: ", so_row, "x", so_col, "x", ICt)
            print("Number of square-inclined window:", N_parallel_window_so(image,kernel,so_row,so_col))
            if marginal_optimizable_row(image, kernel, so_row):
              marginal_space_row = (image-so_row) % (so_row - kernel +1)
              # print("marginal_space_row is",marginal_space_row) # 4
              moX_row = marginal_space_row + kernel - 1
              moX_col = (pw_row * pw_col) // moX_row
              ICmX = ar // (moX_row * moX_col)
              No_of_moX = math.ceil(((image-moX_col)/(moX_col - kernel +1)))+1
              # print("Marginal_window_row:", moX_row, "x", moX_col, ", and No_of_marginal_window_X is", No_of_moX)
              print("Marginal_window_row:", moX_row, "x", moX_col, "x", ICmX)
              print("No_of_marginal_window_row:", No_of_moX)
            else:
              # print("There is no marginal rows to be optimzed.")
              No_of_moX=0

            if marginal_optimizable_col(image, kernel, so_col):
              marginal_space_col = (image-so_col) % (so_col - kernel +1)
              # print("marginal_space_col is",marginal_space_col) # 4
              moY_col = marginal_space_col + kernel - 1
              moY_row = (pw_row * pw_col) // moY_col
              ICmY = ar // (moY_row * moY_col)
              No_of_moY = math.ceil(((image-moY_row)/(moY_row - kernel +1)))+1
              # print("marginal_window_size on cols has size", moY_row, "x", moY_col, ", and No_of_marginal_window_Y is", No_of_moY)
              print("Marginal_window_column:", moY_row, "x", moY_col, "x", ICmY)
              print("No_of_marginal_window_column:", No_of_moY)
            else:
              # print("There is no marginal cols to be optimzed.")
              No_of_moY=0

            No_windows_so = N_parallel_window_so(image,kernel,so_row,so_col)
            No_windows = ( No_windows_so + No_of_moX + No_of_moY )
            # print("!!!!!N_parallel_window_so is!!!!", No_windows_so)
            print("Number of square-inclined window and marginal window (one-tile):", No_windows)

          else:
            # print("This pair is not optimized")
            No_windows = N_parallel_window(image,kernel,sw_row,sw_col)

  if found_so == False:
            # print("found_so", found_so)
            if marginal_optimizable_row(image, kernel, pw_row):
              marginal_space_row = (image-pw_row) % (pw_row - kernel +1)
              # print("marginal_space_row is",marginal_space_row) # 4
              moX_row = marginal_space_row + kernel - 1
              moX_col = (ar/pw_ic) // moX_row
              ICmX = ar // (moX_row * moX_col)
              No_of_moX = math.ceil(((image-moX_col)/(moX_col - kernel +1)))+1
              # print("marginal_window_size on rows has size", moX_row, "x", moX_col, ", and No_of_marginal_window_X is", No_of_moX)
              print("Marginal_window_row:", moX_row, "x", moX_col, "x", ICmX)
              print("No_of_marginal_window_row:", No_of_moX)
            else:
              # print("There is no marginal rows to be optimzed.")
              No_of_moX=0

            if marginal_optimizable_col(image, kernel, pw_col):
              marginal_space_col = (image-pw_col) % (pw_col - kernel +1)
              print("marginal_space_col is",marginal_space_col) # 4
              moY_col = marginal_space_col + kernel - 1
              moY_row = (ar/pw_ic) // moY_col
              ICmY = ar // (moY_row * moY_col)
              No_of_moY = math.ceil(((image-moY_row)/(moY_row - kernel +1)))+1
              # print("marginal_window_size on cols has size", moY_row, "x", moY_col, ", and No_of_marginal_window_Y is", No_of_moY)
              print("Marginal_window_column:", moY_row, "x", moY_col, "x", ICmY)
              print("No_of_marginal_window_column:", No_of_moY)
            else:
              # print("There is no marginal cols to be optimzed.")
              No_of_moY=0

            No_windows_so = N_parallel_window_so(image,kernel,pw_row,pw_col)
            No_windows = ( No_windows_so + No_of_moX + No_of_moY )
            print("No square-inclined window can be found. Number of windows:", No_windows_so, "for", pw_row,"x", pw_col )
            print("Number of windows with marginal-optimized:", No_windows)


# calculate variable depeth
  # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  remaining_channels = ic % ICt
  reg_remaining_channels = remaining_channels
  # print("Remaining channels: ", remaining_channels)
  No_windows = No_windows * (ic // ICt)
  print("Total number of windows with square-optimized, marginal-optimized is", No_windows)
  max_conv = ac // oc #16
  # print("Maximum convolution: ", max_conv)
  found_max = False
  found_conv = False
  # found_so = False
          # No_remaining_parallel_window

  prune = 0

  while found_max==False and (remaining_channels >0):
    # try:
      print("PRUNING", prune, "CHANNELS")
      remaining_channels -= prune
      print("Remaining channels", remaining_channels)
      for i in range(int(pow(max_conv, 1 / 2))+1,1, -1):
        if (max_conv % i == 0) and (int(max_conv / i) <= image):
                  # print("FACTOR: " + str(i) +"*"+str(int(max_conv / i)))
                  dw_row = i + kernel -1
                  dw_col = int(max_conv / i) + kernel -1
                  # print("Depth_optimal_window is", dw_row, "*", dw_col)
                  # print("Number of window is", N_parallel_window(image,kernel,dw_row,dw_col))
                  if marginal_optimizable_row(image, kernel, dw_row):
                          print(image,kernel,dw_row)
                          mmarginal_space_row = (image-dw_row) % (dw_row - kernel +1)
                          # print("marginal_space_row is",mmarginal_space_row) # 2
                          mmoX_row = mmarginal_space_row + kernel - 1 #6
                          mmoX_col = (ar / pw_ic) // mmoX_row
                          mICmX = ar // (mmoX_row * mmoX_col)
                          No_of_mmoX = math.ceil(((image-mmoX_col)/(mmoX_col - kernel +1)))+1
                          # print("marginal_window_size on rows has size", moX_row, "x", moX_col, ", and No_of_marginal_window_X is", No_of_moX)
                          print("Marginal_window_row:", moX_row, "x", moX_col, "x", mICmX)
                          print("No_of_marginal_window_row:", No_of_moX)
                  else:
                          # print("There is no marginal rows to be optimzed.")
                          No_of_mmoX =0

                  if marginal_optimizable_col(image, kernel, dw_col):
                          mmarginal_space_col = (image-dw_col) % (dw_col - kernel +1)
                          print("marginal_space_col is",mmarginal_space_col) # 1
                          mmoY_col = mmarginal_space_col + kernel - 1 #3
                          mmoY_row = (pw_row * pw_col) // mmoY_col #7
                          mICmY = ar // (mmoY_row * mmoY_col)
                          No_of_mmoY = math.ceil(((image-mmoY_row)/(mmoY_row - kernel +1)))+1
                          # print("marginal_window_size on cols has size", moY_row, "x", moY_col, ", and No_of_marginal_window_Y is", No_of_moY)
                          print("Marginal_window_column:", moY_row, "x", moY_col, "x", mICmY)
                          print("No_of_marginal_window_column:", No_of_moY)
                  else:
                          # print("There is no marginal cols to be optimzed.")
                          No_of_mmoY=0

            #               No_windows_so = N_parallel_window_so(image,kernel,so_row,so_col)
            # No_windows = ( No_windows_so + No_of_moX + No_of_moY )
                  No_window_with_marginal = N_parallel_window_so(image,kernel,dw_row,dw_col) + No_of_mmoX + No_of_mmoY
                  # print("No_window_with_marginal：",No_window_with_marginal)

                  # No_windows += optimal_N_parallel_window + No_of_mmoX + No_of_mmoY
                  if (No_window_with_marginal<= No_remaining_parallel_window) and (dw_row*dw_col * (remaining_channels) <= ar) :
                      found_max = True
                      optimal_N_parallel_window = N_parallel_window(image,kernel,dw_row,dw_col)
                      do_row = dw_row
                      do_col = dw_col
                      No_cells_do = dw_row*dw_col
                      mICt = ar // No_cells_do
                      # N_parallel_window_so(image,kernel,so_row,so_col)
                      # print("Depth-optimal window:", do_row, "x", do_col, "is better than the original PW", pw_row, pw_col)
                      print("Depth-optimal window:", do_row, "x", do_col, "x",mICt)
                      # print(optimal_N_parallel_window, "optimal_N_parallel_window")
                      No_windows += No_window_with_marginal
                      print("OVERALL Computing Cycle:", No_windows)
                      break
                  # else:
                      # print("This pair is not allowed")


      prune =1




  return No_windows

# #cnn8-3
# image, kernel, ic, oc, ar, ac = 18, 3, 32, 32, 512, 512
# pw_row, pw_col, pw_ic, pw_oc = 8, 4, 16, 32

# #cnn8-5,6
# # image, kernel, ic, oc, ar, ac = 7, 3, 64, 64, 512, 512
# # pw_row, pw_col, pw_ic, pw_oc = 7, 3, 24, 64

# #LeNet5-3
# # image, kernel, ic, oc, ar, ac = 14, 5, 6, 16, 512, 512
# # pw_row, pw_col, pw_ic, pw_oc = 9, 8, 6, 16

# #vgg7-2
# # image, kernel, ic, oc, ar, ac = 150, 3, 32, 32, 512, 512
# # pw_row, pw_col, pw_ic, pw_oc = 8, 4, 16, 32

# # cnn4-2
# # image, kernel, ic, oc, ar, ac = 28, 5, 16, 32, 512, 512
# # pw_row, pw_col, pw_ic, pw_oc = 9, 7, 8, 32

# print("="*50)
# print("INFORMATION")
# print("-"*30)
# print("    Array   Size = {} x {}".format(ar, ac))
# print("    Image   Size = {} x {}".format(image, image))
# print("    Kernel  Size = {} x {}".format(kernel, kernel))
# print("    Channel Size = {} x {}".format(ic, oc))

# print("="*50)
# print("    RESULTS of COMPUTING CYCLES")
# print("-"*30)
# tetris_cc(image, kernel, ic, oc, ar, ac, pw_row, pw_col, pw_ic, pw_oc)
# print("="*50)

# Network configurations
network_configs = {
    'cnn8-3': (18, 3, 32, 32, 512, 512, 8, 4, 16, 32),
    'cnn8-5': (7, 3, 64, 64, 512, 512, 7, 3, 24, 64),
    'LeNet5-3': (14, 5, 6, 16, 512, 512, 9, 8, 6, 16),
    'vgg7-2': (150, 3, 32, 32, 512, 512, 8, 4, 16, 32),
    'cnn4-2': (28, 5, 16, 32, 512, 512, 9, 7, 8, 32)
    # Add more network configurations as needed
}

if __name__ == "__main__":
    # Ask for user input
    network_key = input("Enter network configuration key (e.g., cnn8-3): ")

    # Retrieve the configuration
    if network_key in network_configs:
        image, kernel, ic, oc, ar, ac, pw_row, pw_col, pw_ic, pw_oc = network_configs[network_key]

        # Display Information
        print("="*50)
        print("INFORMATION")
        print("-"*30)
        print("    Array   Size = {} x {}".format(ar, ac))
        print("    Image   Size = {} x {}".format(image, image))
        print("    Kernel  Size = {} x {}".format(kernel, kernel))
        print("    Channel Size = {} x {}".format(ic, oc))

        # Results
        print("="*50)
        print("    RESULTS of COMPUTING CYCLES")
        print("-"*30)
        tetris_cc(image, kernel, ic, oc, ar, ac, pw_row, pw_col, pw_ic, pw_oc)
        print("="*50)
    else:
        print("Network configuration not found.")