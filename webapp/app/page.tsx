"use client";

import "@wonderflow/react-components/core.css";
import "@wonderflow/themes";
import {
  ResponsiveProvider,
  Container,
  Grid,
  ProductCard,
} from "@wonderflow/react-components";
import useSWR from "swr";
import pkg from "../package.json";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function Home() {
  const { data, error, isLoading } = useSWR("/api/beers", fetcher);

  if (isLoading) return <div>loading...</div>;
  console.log(data);
  return (
    // <ResponsiveProvider>
    <Container dimension="large" padding>
      <Grid columnGap={48} rowGap={48}>
        {data.data.map((beer) => {
          return (
            <Grid.Item>
              c
              <ProductCard
                key={beer.name}
                subtitle="Beer"
                title={beer.name}
                source={[beer.image]}
                priceMin={beer.price}
                feedbackCount={123}
                // menuActions={<Menu>...</Menu>}
              />
            </Grid.Item>
          );
        })}
      </Grid>
    </Container>
    // </ResponsiveProvider>
  );
}
