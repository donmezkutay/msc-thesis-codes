from shapely.geometry import mapping

import xarray as xr
import numpy as np
import geopandas as gpd
import cartopy

def assign_proj_to_model(dt_model):
    
    # define globe
    globe = cartopy.crs.Globe(ellipse='sphere',
                          semimajor_axis=6370000,
                          semiminor_axis=6370000)
    
    # projection info
    dt_proj = xr.open_dataset(fr'data/lffd2100123118.nc')
    
    # fetch model projection info
    rotated_pole = dt_proj['rotated_pole']
    pole_longitude = rotated_pole.attrs['grid_north_pole_longitude']
    pole_latitude = rotated_pole.attrs['grid_north_pole_latitude']
    
    # define model projection
    proj_model = cartopy.crs.RotatedPole(pole_longitude=pole_longitude,
                                   pole_latitude=pole_latitude,
                                   globe=globe
                                   )
    
    # x and y dims
    dt_x_dim_model = 'rlon'
    dt_y_dim_model = 'rlat'

    # write projection
    dt_model = dt_model.rio.write_crs(proj_model)

    # set spatial dims
    dt_model = dt_model.rio.set_spatial_dims(x_dim=dt_x_dim_model,
                                             y_dim=dt_y_dim_model)
    
    return dt_model

def assign_proj_to_era5(dt_era5, regrid=False):
    
    # define observation projection
    proj_obs = cartopy.crs.CRS('EPSG:4326',
                              )
    
    # x and y dims
    dt_x_dim_obs = 'longitude'
    dt_y_dim_obs = 'latitude'
    
    if regrid == True:
        dt_x_dim_obs = 'y'
        dt_y_dim_obs = 'x'

    # write projection
    dt_era5 = dt_era5.rio.write_crs(proj_obs)

    # set spatial dims
    dt_era5 = dt_era5.rio.set_spatial_dims(x_dim=dt_x_dim_obs,
                                           y_dim=dt_y_dim_obs)
    
    return dt_era5

def regrid_match(dt_to_match, dt_to_be_matched):
    
    """
    Regrid a file grid to a target grid. Requires input data array
    
    Return target file and regridded file
    
    """
    # reproject
    dt_to_be_matched = dt_to_be_matched.rio.reproject_match(dt_to_match)
    
    return dt_to_be_matched

def discard_nodata_problem(data):
    
    nodata = data.rio.nodata
    data = data.where(data!=nodata, np.nan)
    
    return data
    
def get_proj_info_model():
    
    # define globe
    globe = cartopy.crs.Globe(ellipse='sphere',
                          semimajor_axis=6370000,
                          semiminor_axis=6370000)
    
    # projection info
    dt_proj = xr.open_dataset(fr'data/lffd2100123118.nc')
    
    # fetch model projection info
    rotated_pole = dt_proj['rotated_pole']
    pole_longitude = rotated_pole.attrs['grid_north_pole_longitude']
    pole_latitude = rotated_pole.attrs['grid_north_pole_latitude']
    
    # define model projection
    proj_model = cartopy.crs.RotatedPole(pole_longitude=pole_longitude,
                                   pole_latitude=pole_latitude,
                                   globe=globe
                                   )
    
    return proj_model

def clip_to_city(data, shapefile):
    
    clipped = data.rio.clip(shapefile.geometry.apply(mapping),
                            shapefile.crs, all_touched=True, 
                            invert=False, from_disk=True)
    
    return clipped