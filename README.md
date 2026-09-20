# CT-NIfTI Boundary Pipeline

A Python-based workflow for extracting simulation-ready boundary surfaces from CT-derived NIfTI volumes.

## Overview

This project demonstrates the conversion of voxel-based medical/engineering image data into physical-coordinate boundary representations suitable for numerical simulation workflows.

The pipeline focuses on:

- NIfTI volume handling
- coordinate transformation
- boundary surface extraction
- STL generation
- metadata preparation

## Background

Developed from a Digital Engineering research project at Bauhaus-Universität Weimar.

The original project investigated image-to-analysis workflows for CT-based fracture simulation.

## My Contribution

My contribution focused on:

- CT/NIfTI data processing workflow
- coordinate consistency between voxel and physical space
- boundary-condition surface extraction
- STL export workflow
- preparation of simulation-ready geometry data

## Workflow

CT / NIfTI volume

    ↓

Volume preprocessing

    ↓

Boundary extraction

    ↓

STL surface generation

    ↓

Simulation-ready output

## Technologies

- Python
- NumPy
- NiBabel
- PyVista
- STL processing
- Git

## Project Status

Currently under reconstruction as a clean portfolio implementation.