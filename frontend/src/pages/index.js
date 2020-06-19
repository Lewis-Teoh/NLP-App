import React, { useEffect, useState } from "react"
import {
  Grid,
  Card,
  CardMedia,
  CardContent,
  Button,
  Typography,
  makeStyles,
  Divider,
  TextField,
  LinearProgress,
} from "@material-ui/core"
import Layout from "../components/layout"
import img from "../images/item01.png"
import Rating from "@material-ui/lab/Rating"
import axios from "axios"
import { useFormik } from "formik"
import * as Yup from "yup"

const useStyles = makeStyles({
  img: {
    width: 240,
    height: 240,
  },
  text_input: {
    width: "100%",
  },
})

const IndexPage = () => {
  const classes = useStyles()
  const [reviews, updateReviews] = useState([])
  const [overallRate, setOverallRate] = useState(0.0)
  const [loading, setLoading] = useState(true)

  const formik = useFormik({
    validateOnBlur: false,
    validateOnChange: false,
    validationSchema: Yup.object().shape({
      rating: Yup.number().min(1).max(5),
      review: Yup.string().required(),
    }),
    initialValues: {
      rating: 0,
      review: "",
    },
    onSubmit: async (values, { resetForm }) => {
      setLoading(true)
      await axios
        .post("http://127.0.0.1:5000/add_review", values)
        .then(response => {
          console.log(response)
          updateReviews(prev => [...prev, values])
          resetForm()
          setLoading(false)
        })
        .catch(err => {
          console.error(err)
        })
    },
  })

  const fetchData = async () => {
    await axios
      .get("http://127.0.0.1:5000/reviews")
      .then(response => {
        updateReviews(response.data.reviews)
        setOverallRate(calcOverallRate(response.data.reviews))
        setLoading(false)
        console.log(response.data.reviews)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }

  const calcOverallRate = reviews => {
    var total = 0.0
    reviews.forEach(element => {
      total += element.rating * 1.0
    })
    return parseFloat(total / reviews.length).toFixed(1)
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <Layout>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <Grid container direction="row">
              <Grid item container justify="center" xs={4}>
                <CardMedia
                  className={classes.img}
                  component="img"
                  height="140"
                  image={img}
                />
              </Grid>
              <Grid item xs={8}>
                <CardContent>
                  <Typography variant="h5" component="h2">
                    Sony WH-1000MX3
                  </Typography>
                  <Typography
                    variant="body2"
                    color="textSecondary"
                    component="p"
                  >
                    WH-1000XM3 headphones take you even deeper into silence with
                    further improvements to our industry-leading noise
                    cancellation1, and smart listening that adjusts to your
                    situation.
                  </Typography>
                  <Typography variant="h5" component="h2">
                    RM 1000.00
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item>
                      <Button variant="contained">Buy now</Button>
                    </Grid>
                    <Grid item>
                      <Button variant="contained">Add to cart</Button>
                    </Grid>
                  </Grid>
                </CardContent>
              </Grid>
            </Grid>
          </Card>
        </Grid>

        <Grid item xs={12}>
          {loading ? <LinearProgress /> : null}
          <Card>
            <CardContent>
              <Grid container direction="column" spacing={2}>
                <Grid item>
                  <Typography>{overallRate}/5.0</Typography>

                  <Typography>{reviews.length} ratings</Typography>
                </Grid>
                <Grid item>
                  <Divider />
                </Grid>
                <Grid item container spacing={2}>
                  <Grid item xs={12}>
                    <Rating
                      id="rating"
                      name="rating"
                      type="number"
                      value={formik.values.rating}
                      onChange={(_, value) => {
                        formik.setFieldValue("rating", value)
                      }}
                    />
                  </Grid>
                  <Grid item xs={9}>
                    <TextField
                      className={classes.text_input}
                      id="review"
                      name="review"
                      label="Your Review"
                      multiline
                      rowsMax={5}
                      variant="outlined"
                      value={formik.values.review}
                      onChange={formik.handleChange}
                    />
                  </Grid>
                  <Grid item container xs={3} alignItems="center">
                    <Button variant="contained" onClick={formik.handleSubmit}>
                      Submit
                    </Button>
                  </Grid>
                </Grid>
                <Grid item>
                  <Divider />
                </Grid>
                <Grid item container direction="column" spacing={2}>
                  {reviews.map((v, i) => {
                    return (
                      <Grid item key={i}>
                        <Rating value={v.rating} readOnly />
                        <Typography>{v.review}</Typography>
                      </Grid>
                    )
                  })}
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Layout>
  )
}

export default IndexPage
