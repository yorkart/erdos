use pyo3::prelude::*;

use crate::dataflow::{LoopStream, ReadStream};

use super::PyReadStream;

#[pyclass]
pub struct PyLoopStream {
    loop_stream: LoopStream<Vec<u8>>,
}

#[pymethods]
impl PyLoopStream {
    #[new]
    fn new(obj: &PyRawObject) {
        obj.init(Self {
            loop_stream: LoopStream::new(),
        });
    }

    fn set(&self, _py: Python, read_stream: &PyReadStream) {
        self.loop_stream.set(&read_stream.read_stream);
    }

    fn to_py_read_stream(&self, _py: Python) -> PyReadStream {
        PyReadStream::from(ReadStream::from(&self.loop_stream))
    }
}
