import { faker } from '@faker-js/faker';

// ----------------------------------------------------------------------

const POST_TITLES = [
  'Wall Street Managers Are Pushing Back on Easing Inflation Hopes',
  'Warren Buffett says he doesn’t own bitcoin because ‘it isn’t going to do anything’ — he’d rather own these 2 productive assets instead',
  'Electric Vehicles Require Lots of Scarce Parts. Is the Supply Chain Up to It?', 
  'Exclusive: As split Congress odds increase, Yellen warns of need to lift debt ceiling',
  'What You Need to Know Before Gifting a 529 Plan',
  'The Epic Collapse of Sam Bankman-Fried’s DeFi Empire',
  'FTX’s Bankman-Fried Interviewed by Bahamas Police, Regulators',
  'Democrats Retain Control of US Senate With Nevada Victory',
  'Stocks making the biggest moves midday: Walgreens, Coinbase, Duolingo, Ralph Lauren and more',
  'Europe Poised for a Warmer-than-Normal Winter, Copernicus Says',
  "Delivery Hero heads for strongest weekly gain on record",
  'The American Dream retold through mid-century railroad graphics',
];

const posts = [...Array(11)].map((_, index) => ({
  id: faker.datatype.uuid(),
  cover: `/assets/images/covers/cover_${index + 1}.jpg`,
  title: POST_TITLES[index + 1],
  createdAt: faker.date.past(),
  view: faker.datatype.number(),
  comment: faker.datatype.number(),
  share: faker.datatype.number(),
  favorite: faker.datatype.number(),
  author: {
    name: faker.name.fullName(),
    avatarUrl: `/assets/images/avatars/avatar_${index + 1}.jpg`,
  },
}));

export default posts;
