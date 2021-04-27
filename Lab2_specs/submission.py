## import modules here 
import pandas as pd
import numpy as np
import helper


################### Question 1 ###################

def project_data(df, d):
    # Return only the d-th column of INPUT
    return df.iloc[:, d]

def select_data(df, d, val):
    # SELECT * FROM INPUT WHERE input.d = val
    col_name = df.columns[d]
    return df[df[col_name] == val]

def remove_first_dim(df):
    # Remove the first dim of the input
    return df.iloc[:, 1:]

def slice_data_dim0(df, v):
    # syntactic sugar to get R_{ALL} in a less verbose way
    df_temp = select_data(df, 0, v)
    return remove_first_dim(df_temp)


def single_tuple_result_print_out(df):
    
    # if there is only one column left
    # which is the base case
    if df.shape[1] == 1:
        return df
    else:
        # the idea is to append dataframe
        # 1  2
        # 1  *
        # *  2
        # *  *
        first_dimension = df.columns[0]
        remain_df = df.drop(first_dimension, axis=1)
        inner_df = single_tuple_result_print_out(remain_df)
        inner_df_copy = inner_df.copy()
        # first df with column of value 1
        inner_df.insert(0, first_dimension, df.iloc[0][first_dimension])
        # second df with column of value *
        inner_df_copy.insert(0, first_dimension, df.iloc[1][first_dimension])

        result = pd.concat([inner_df, inner_df_copy], ignore_index=True)
    return result

def single_tuple(df):
    
# append a star row at the bottom 
# in order to do the simple_tuple_optimization
    num_of_stars = len(list(df))-1
    star_array = []
    for i in range (num_of_stars):
        star_array.append('ALL')
    # add a row of stars and M value at the last
    star_array.append(df.iloc[0][df.columns[-1]])
    df.loc['1'] = star_array

    # the dataframe without the 'M' column
    dimension_df = df.drop(df.columns[-1], axis=1)
    # get the result of single_tuple
    
    result = single_tuple_result_print_out(dimension_df)
    # Add a uniform M value to the last column
    result['M'] = df.iloc[0][df.columns[-1]]
    
    return result
#=================================================================================

def buc_rec_optimized(df):# do not change the heading of the function
    
    dimensionlist = list(df)[0:-1] # produce A, B
    
    result = pd.DataFrame(columns=list(df))
    
    df_1 = project_data(df,0)
    df_2 = slice_data_dim0(df,0)



    for index, dimension in enumerate(dimensionlist):
        dimension_uniq_value_list = df[dimension].unique() # [1,2]
        for dim_value in dimension_uniq_value_list:
            dim_df = select_data(df, index, dim_value)
            if dim_df.shape[0] == 1: # check whether it is a single tuple
                result = pd.concat([result, single_tuple(dim_df)], ignore_index=True)
            else:
                sliced_df = remove_first_dim(dim_df)
                sub_result = buc_rec_optimized(sliced_df)
                sub_result_copy = sub_result.copy()
                sub_result.insert(0, dimension, dim_value) # append column A
                
                sub_result_copy.insert(0, dimension, 'ALL')
                
                partial_result = pd.concat([sub_result, sub_result_copy], ignore_index=True)
                
                result = pd.concat([result, partial_result], ignore_index=True)
        break

    aggregation_functions = {'M': 'sum'}
    df_new = result.groupby(dimensionlist,as_index=False).aggregate(aggregation_functions)
    return df_new


