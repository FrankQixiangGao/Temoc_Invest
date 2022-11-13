import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { FormControl, InputLabel, Input, FormHelperText } from '@mui/material';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
  minWidth: "800px",
};

export default function BasicModal({open, handleClose}) {
  return (
    <div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <div>
            <FormControl fullWidth>
              <InputLabel htmlFor="my-input">Portfolio annualized return rate</InputLabel>
              <Input id="my-input" aria-describedby="my-helper-text" />
              <FormHelperText id="my-helper-text">annualized return rate</FormHelperText>
            </FormControl>
          </div>
          <div>
            <FormControl fullWidth>
              <InputLabel htmlFor="my-input">Max risk level</InputLabel>
              <Input id="my-input" aria-describedby="my-helper-text" />
              <FormHelperText id="my-helper-text">risk level</FormHelperText>
            </FormControl>
          </div>
          <div>
            <Button>Submit</Button>
          </div>
        </Box>
      </Modal>
    </div>
  );
}