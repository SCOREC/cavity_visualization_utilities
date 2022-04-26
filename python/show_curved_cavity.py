import sys, argparse, os, glob

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--root_dir', help="root directory of all cavities")
parser.add_argument('-c', '--cavity_name', help="the specific cavity name")
parser.add_argument('-p', '--save_png', help="saves a png of the view", action="store_true")
parser.add_argument('-m', '--show_mesh', help="show mesh", action="store_true")
args = parser.parse_args()


def get_vtu_path_for_mesh(root, vtu_phrase):
  identifier='curved'
  search_phrase=root+"/mesh/"+identifier+"/rep_tri_*"
  all_ = glob.glob(search_phrase)
  target_dir = ''
  if (len(all_) == 1):
    target_dir=all_[0]
  else:
    max_res=-1
    max_idx=0
    idx=0
    for st in all_:
      substs = st.split("_")
      if substs[-2] > max_res:
	max_res = substs[-2]
	max_idx = idx
      idx=idx+1
    target_dir=all_[max_idx]
  search_phrase=target_dir+"/"+vtu_phrase
  all_vtus=glob.glob(search_phrase)

  if (len(all_vtus) == 0):
    print("no vtu was found in " + search_phrase + ". quiting!")
    sys.exit("Exiting!")

  target_vtu=''
  if (len(all_vtus) == 1):
    target_vtu=all_vtus[0]
  else:
    max_res=-1
    max_idx=0
    idx=0
    for st in all_vtus:
      substs = st.split("_")
      if substs[-2] > max_res:
	max_res = substs[-2]
	max_idx = idx
      idx=idx+1
    target_vtu=all_vtus[max_idx]
  return target_vtu
# end of get_vtu_path_for_mesh

def get_vtu_path_for_cavity(root, cavity_name, curved=True):
  is_vertex_cavity=False
  if cavity_name.split('_')[-2] == "vertex":
    is_vertex_cavity=True
  all_cavities = glob.glob(root+"/cavities/*")
  all_cavities_short = [name.split("/")[-1] for name in all_cavities]
  if cavity_name not in all_cavities_short:
    print(cavity_name, "was not found in ", root+"/cavities")
    print("available names are:")
    print(all_cavities_short)
    sys.exit("Exiting!")


  if curved:
    search_phrase=root+"/cavities/"+cavity_name+"/cavity_curved/rep_tri_*"
    all_rep_tri_folders=glob.glob(search_phrase)

    target_dir = ''
    if (len(all_rep_tri_folders) == 1):
      target_dir=all_rep_tri_folders[0]
    else:
      max_res=-1
      max_idx=0
      idx=0
      for st in all_rep_tri_folders:
	substs = st.split("_")
	if substs[-2] > max_res:
	  max_res = substs[-2]
	  max_idx = idx
	idx=idx+1
      target_dir=all_rep_tri_folders[max_idx]

    search_phrase=target_dir+"/vtu/order_*.vtu"
    all_vtus=glob.glob(search_phrase)

    if (len(all_vtus) == 0):
      print("no vtu was found in ", search_phrase, ". quiting!")
      sys.exit("Exiting!")


    target_vtu=''
    if (len(all_vtus) == 1):
      target_vtu=all_vtus[0]
    else:
      max_res=-1
      max_idx=0
      idx=0
      for st in all_vtus:
	substs = st.split("_")
	if substs[-2] > max_res:
	  max_res = substs[-2]
	  max_idx = idx
	idx=idx+1
      target_vtu=all_vtus[max_idx]

    cavity_path=target_vtu

    search_phrase=root+"/cavities/"+cavity_name+"/cavity_curved_wire/0/*.vtu"
    vtu_files=glob.glob(search_phrase)
    if (len(vtu_files) == 0):
      print("no vtu was found in ", search_phrase, ". quiting!")
      sys.exit("Exiting!")
    cavity_wire_path=vtu_files[0]


    if is_vertex_cavity:
      search_phrase=root+"/cavities/"+cavity_name+"/entity_linear/0/*.vtu"
    else:
      search_phrase=root+"/cavities/"+cavity_name+"/entity_curved_wire/0/*.vtu"
    entity_vtu=glob.glob(search_phrase)

    if (len(entity_vtu) == 0):
      print("no vtu was found in ", search_phrase, ". quiting!")
      sys.exit("Exiting!")
    entity_path=entity_vtu[0]
  else:
    search_phrase=root+"/cavities/"+cavity_name+"/cavity_linear/0/*.vtu"
    vtu_files=glob.glob(search_phrase)
    if (len(vtu_files) == 0):
      print("no vtu was found in ", search_phrase, ". quiting!")
      sys.exit("Exiting!")
    cavity_path=vtu_files[0]
    cavity_wire_path=cavity_path

    search_phrase=root+"/cavities/"+cavity_name+"/entity_linear/0/*.vtu"
    vtu_files=glob.glob(search_phrase)
    if (len(vtu_files) == 0):
      print("no vtu was found in ", search_phrase, ". quiting!")
      sys.exit("Exiting!")
    entity_path=vtu_files[0]
  return cavity_path, cavity_wire_path, entity_path
# end of get_vtu_path_for_cavity


# construct the mesh_path
# vtu_phrase="vtu/order_*"
mesh_path=get_vtu_path_for_mesh(args.root_dir, "vtu/order_*")

cavity_path, cavity_wire_path, entity_path = get_vtu_path_for_cavity(args.root_dir, args.cavity_name)

#### ParaView Related Code

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1994, 1260]

# create a new 'XML Unstructured Grid Reader'
order_3_0vtu = XMLUnstructuredGridReader(FileName=[mesh_path])
order_3_0vtu.PointArrayStatus = ['detJacobian']
# show data in view
order_3_0vtuDisplay = Show(order_3_0vtu, renderView1)
# trace defaults for the display properties.
order_3_0vtuDisplay.ColorArrayName = [None, '']
order_3_0vtuDisplay.DiffuseColor = [1,1,1]
order_3_0vtuDisplay.EdgeColor = [0.0, 0.0, 0.2]
order_3_0vtuDisplay.BackfaceDiffuseColor = [1,1,1]
order_3_0vtuDisplay.ScalarOpacityUnitDistance = 0.05

# reset view to fit data
renderView1.ResetCamera()

# Properties modified on order_3_0vtuDisplay
order_3_0vtuDisplay.Opacity = 0.05

if not args.show_mesh:
  Hide(order_3_0vtu, renderView1)

# create a new 'XML Unstructured Grid Reader'
order_3_0vtu_1 = XMLUnstructuredGridReader(FileName=[cavity_path])
order_3_0vtu_1.PointArrayStatus = ['detJacobian']

# show data in view
order_3_0vtu_1Display = Show(order_3_0vtu_1, renderView1)
# trace defaults for the display properties.
order_3_0vtu_1Display.ColorArrayName = [None, '']
order_3_0vtu_1Display.DiffuseColor = [1,1,1]
order_3_0vtu_1Display.EdgeColor = [0.0, 0.0, 0.2]
order_3_0vtu_1Display.BackfaceDiffuseColor = [1,1,1]
order_3_0vtu_1Display.ScalarOpacityUnitDistance = 0.05

# Properties modified on order_3_0vtu_1Display
order_3_0vtu_1Display.Opacity = 0.5

# create a new 'XML Partitioned Unstructured Grid Reader'
cavity_curved_wirepvtu = XMLUnstructuredGridReader(FileName=[cavity_wire_path])
cavity_curved_wirepvtu.CellArrayStatus = ['apf_part']

# show data in view
cavity_curved_wirepvtuDisplay = Show(cavity_curved_wirepvtu, renderView1)
# trace defaults for the display properties.
cavity_curved_wirepvtuDisplay.ColorArrayName = [None, '']
cavity_curved_wirepvtuDisplay.DiffuseColor = [1,1,1]
cavity_curved_wirepvtuDisplay.EdgeColor = [0.0, 0.0, 0.2]
cavity_curved_wirepvtuDisplay.BackfaceDiffuseColor = [1,1,1]
cavity_curved_wirepvtuDisplay.ScalarOpacityUnitDistance = 0.05

# change solid color
cavity_curved_wirepvtuDisplay.DiffuseColor = [0.0, 0.0, 0.0]

# Properties modified on cavity_curved_wirepvtuDisplay
cavity_curved_wirepvtuDisplay.LineWidth = 2.0

entity_curved_wirepvtu = XMLUnstructuredGridReader(FileName=[entity_path])
entity_curved_wirepvtu.CellArrayStatus = ['apf_part']

# show data in view
entity_curved_wirepvtuDisplay = Show(entity_curved_wirepvtu, renderView1)
# trace defaults for the display properties.
entity_curved_wirepvtuDisplay.ColorArrayName = [None, '']
entity_curved_wirepvtuDisplay.DiffuseColor = [1,1,1]
entity_curved_wirepvtuDisplay.EdgeColor = [0.0, 0.0, 0.2]
entity_curved_wirepvtuDisplay.BackfaceDiffuseColor = [1,1,1]
entity_curved_wirepvtuDisplay.ScalarOpacityUnitDistance = 0.05383165162830335

# change solid color
entity_curved_wirepvtuDisplay.DiffuseColor = [1., 0.0, 0.0]

# Properties modified on entity_curved_wirepvtuDisplay
entity_curved_wirepvtuDisplay.LineWidth = 3.0

# current camera placement for renderView1
renderView1.CameraPosition = [0.6710013769621432, -2.2271728114780966, 1.4479305503461593]
renderView1.CameraFocalPoint = [-0.03598978194513412, -0.03951699619474098, -0.0896753010948714]
renderView1.CameraViewUp = [-0.16063543985271023, 0.5322885008784687, 0.8311830167272903]
renderView1.CameraParallelScale = 0.7158537199797246

#### uncomment the following to render all views
if args.save_png:
  png_name = args.cavity_name+".png"
  SaveScreenshot(png_name)

RenderAllViews()
Interact()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
