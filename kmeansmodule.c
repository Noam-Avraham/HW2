#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <math.h>

double distance(double* point1, double* point2, int dim) {
    double sum = 0.0;
    double diff;
    for(int i = 0; i < dim; i++) {
        diff = point1[i] - point2[i];
        sum += diff * diff;
    }
    return sqrt(sum);
}
double add_vectors(double* vec1, double* vec2, int dim,int opertion) {
    int i;
    for(i = 0; i < dim; i++) {
        vec1[i] += vec2[i]*opertion;
    }
    return 0;
}
double* copy_vector(double* src, int dim) {
    int i;
    double* dest;
    dest=(double*)malloc(dim * sizeof(double));
    for(i = 0; i < dim; i++) {
        dest[i] = src[i];
    }   
    return dest;
}
double update_clusters(double** points, double** clusters, int* points_to_cluster,double** clusters_sums,int* clusters_counts, int k, int dim, int n, double epsilon) {
    /** reassign the first point to empty cluster */
    int i,j;
    double max_changed;
    double distance_change;
    int previous_index;
    double* cluster_temp;
    /** handle empty clusters */
    for (i = 0; i < k; i++) {
        if (clusters_counts[i]==0)
        {
            previous_index= points_to_cluster[0];
            points_to_cluster[0]=i;
            for(j = 0; j < dim; j++) {
                clusters_sums[previous_index][j]-= points[0][j];
                clusters_sums[i][j]+=points[0][j];
            } 
        clusters_counts[i]++;
        clusters_counts[previous_index]--;
        }
    }
       
    /** calculate new clusters centers */
    for(i = 0; i < k; i++) {
        cluster_temp=copy_vector(clusters[i],dim);
        if(clusters_counts[i] > 0) {
            for(j = 0; j < dim; j++) {
                clusters[i][j] = clusters_sums[i][j] / clusters_counts[i];
            }
        }
        distance_change = distance(cluster_temp, clusters[i], dim);
        free(cluster_temp);
        if (i == 0 || distance_change > max_changed) {
            max_changed = distance_change;
        }
    }
    return max_changed;
}
void update_points(double** points, double** clusters, int* points_to_cluster,double** clusters_sums, int* clusters_counts, int k, int dim, int n) {
    /** assign each point to the nearest cluster */
    int i,j;
    double min_dist, dist;
    int closest_cluster_index;
    int old_index;
    double max_changed;
    for(i = 0; i < n; i++) {
        min_dist = distance(points[i], clusters[0], dim);
        closest_cluster_index = 0;
        old_index = points_to_cluster[i];
        for(j = 1; j < k; j++) {
            dist = distance(points[i], clusters[j], dim);
            if(dist < min_dist) {
                min_dist = dist;
                closest_cluster_index = j;
            }
        }
        if(closest_cluster_index != old_index) {
            points_to_cluster[i] = closest_cluster_index;
            clusters_counts[closest_cluster_index]++;
            add_vectors(clusters_sums[closest_cluster_index], points[i], dim, 1);
            clusters_counts[old_index]--;
            add_vectors(clusters_sums[old_index], points[i], dim, -1);
        }

    }
}

static PyObject* fit(PyObject* self, PyObject* args) {
    /**parse the input from python */
    PyObject *clusters_obj ,*points_obj, *points_to_cluster_obj;
    int k, max_iter,n,dim;
    double eps;
    int i,j;
    int* points_to_cluster;
    double** clusters_sums;
    int assigned_cluster;

    if(!PyArg_ParseTuple(args, "OOOiiiid", &points_obj, &clusters_obj,&points_to_cluster_obj, &k, &max_iter, &dim,&n, &eps)) {
        return NULL;
    }
    points_to_cluster = (int*)malloc(n * sizeof(int));
    clusters_sums = (double**)malloc(k * sizeof(double*));
    /**initalize points to python.points */
    double** points = (double**)malloc(n * sizeof(double*));
    for(i = 0; i < n; i++) {
        points[i] = (double*)malloc(dim * sizeof(double));
        PyObject* point = PyList_GetItem(points_obj, i);
        for(j = 0; j < dim; j++) {
            PyObject* coord =  PyList_GetItem(point, j);
            points[i][j] = PyFloat_AsDouble(coord);
        }
    }
    /**initalize clusters to python.clusters */
    double** clusters = (double**)malloc(k * sizeof(double*));
    for(i = 0; i < k; i++) {
        clusters[i] = (double*)malloc(dim * sizeof(double));
        PyObject* cluster = PyList_GetItem(clusters_obj, i);
        for(j = 0; j < dim; j++) {
            PyObject* coord = PyList_GetItem(cluster, j);
            clusters[i][j] = PyFloat_AsDouble(coord);
        }
    }
    /**initalize points_to_cluster to python.points_to_cluster */

    for(i = 0; i < n; i++) {
        PyObject* cluster_index = PyList_GetItem(points_to_cluster_obj, i);
        points_to_cluster[i] = PyLong_AsLong(cluster_index);
    }
    /**initalize clusters_sums and clusters_counts */
    /*use calloc to initialize clusters_sums */
    for (i = 0; i < k; i++) {
        clusters_sums[i] = (double*)calloc(dim , sizeof(double));
    }
    int* clusters_counts = (int*)calloc(k , sizeof(int));
   
    for(i=0;i<n;i++){
        assigned_cluster=points_to_cluster[i];
        clusters_counts[assigned_cluster]++;
        add_vectors(clusters_sums[assigned_cluster], points[i], dim, 1);
    }
    /** main kmeans loop */
    for(i=0;i<max_iter;i++)
    {
        update_points(points, clusters, points_to_cluster, clusters_sums, clusters_counts, k, dim, n);
        max_changed = update_clusters(points, clusters, points_to_cluster, clusters_sums, clusters_counts, k, dim, n,eps);
        if(max_changed<eps){
            break;
        }
    }
    /**transform result to python array without formatting */
    PyObject* py_result = PyList_New(k);
    for (i = 0; i < k; i++) {
        PyObject* py_finalcluster = PyList_New(dim);
        for (j = 0; j < dim; j++) {
            PyList_SetItem(py_finalcluster, j, PyFloat_FromDouble(clusters[i][j]));
        }
    PyList_SetItem(py_result, i, py_finalcluster);
    }
    return py_result;
}








static PyMethodDef kmeansMethods[] = {
    {"fit",                   
     (PyCFunction)fit,        
     METH_VARARGS,            
     PyDoc_STR("K-means clustering algorithm implementation")}, 
    {NULL, NULL, 0, NULL}     /
};

// הגדרת המודול
static struct PyModuleDef kmeansmodule = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp",            
    NULL,                     
    -1,                       
    kmeansMethods             
};


PyMODINIT_FUNC PyInit_mykmeanssp(void) {
    return PyModule_Create(&kmeansmodule);
}