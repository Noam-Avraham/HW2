#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <math.h>

double distance(double* point1, double* point2, int dim) {
    double sum = 0.0;
    for(int i = 0; i < dim; i++) {
        double diff = point1[i] - point2[i];
        sum += diff * diff;
    }
    return sqrt(sum);
}
double add_vectors(double* vec1, double* vec2, int dim,int opertion) {
    for(int i = 0; i < dim; i++) {
        vec1[i] += vec2[i]*opertion;
    }
    return 0;
}
double copy_vector(double* src, int dim) {
    double* dest=(double*)malloc(dim * sizeof(double));
    for(int i = 0; i < dim; i++) {
        dest[i] = src[i];
    }   
    return dest;
}
void update_clusters(double** points, double** clusters, int* points_to_cluster,double** clusters_sums,int* clusters_counts, int k, int dim, int n) {
    /** reassign the first point to empty cluster */
    for (int i = 0; i < k; i++) {
        clusters_counts[i] = 0;
        int previous_index= points_to_cluster[0];
        points_to_cluster[0]=i;
        for(int j = 0; j < dim; j++) {
            clusters_sums[previous_index][j]-= points[0][j];
            clusters_sums[i][j]+=points[0][j];
        }
    }

}

static PyObject* fit(PyObject* self, PyObject* args) {
    /**parse the input from python */
    PyObject *clusters_obj ,*points_obj, *points_to_cluster_obj;
    int k, max_iter,n,dim;
    double eps;

    if(!PyArg_ParseTuple(args, "OOOiiiid", &points_obj, &clusters_obj,&points_to_cluster_obj, &k, &max_iter, &dim,&n, &eps)) {
        return NULL;
    }
    
    /**initalize points to python.points */
    double** points = (double**)malloc(n * sizeof(double*));
    for(int i = 0; i < n; i++) {
        points[i] = (double*)malloc(dim * sizeof(double));
        PyObject* point = PyList_GetItem(points_obj, i);
        for(int j = 0; j < dim; j++) {
            PyObject* coord =  PyList_GetItem(point, j);
            points[i][j] = PyFloat_AsDouble(coord);
        }
    }
    /**initalize clusters to python.clusters */
    double** clusters = (double**)malloc(k * sizeof(double*));
    for(int i = 0; i < k; i++) {
        clusters[i] = (double*)malloc(dim * sizeof(double));
        PyObject* cluster = PyList_GetItem(clusters_obj, i);
        for(int j = 0; j < dim; j++) {
            PyObject* coord = PyList_GetItem(cluster, j);
            clusters[i][j] = PyFloat_AsDouble(coord);
        }
    }
    /**initalize points_to_cluster to python.points_to_cluster */
    int* points_to_cluster = (int*)malloc(n * sizeof(int));
    for(int i = 0; i < n; i++) {
        PyObject* cluster_index = PyList_GetItem(points_to_cluster_obj, i);
        points_to_cluster[i] = PyLong_AsLong(cluster_index);
    }
    /**initalize clusters_sums and clusters_counts */
    double** clusters_sums = (double**)malloc(k * sizeof(double*));
    for (int i = 0; i < k; i++) {
        clusters_sums[i] = (double*)malloc(dim * sizeof(double));
    }
    int* clusters_counts = (int*)malloc(k * sizeof(int));
   

   

   
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