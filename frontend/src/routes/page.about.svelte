<script context="module">
	import { loading } from '$lib/store.js';

	export async function load({ fetch, session }) {
		loading.set(true);
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}home`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: session.token
			}
		});

		if (_resp.ok) {
			loading.set(false);
			let resp = await _resp.json();

			return {
				props: {
					group: resp.data.group,
					categories: resp.data.categories,
					ads: resp.data.ads
				}
			};
		}
	}
</script>

<script>
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';

	import SVG from '$lib/comp/svg.svelte';
</script>

<Card>
	<Title title="About Us" />
	<Body>
		<section>
			<div class="first">
				<span>Meji</span> is your No. 1 trusted online shopping store in Nigeria where you can
				purchase a wide range of products on the go. Products which includes fashion items for men,
				women, and children; and more. What more? You can have them delivered directly to you.
				<span> Meji </span> guarantees you the safest online shopping payment method, allowing you to
				make stress free payments.
			</div>

			<div class="second">
				<div class="card">
					<SVG size="28" type="time" />
					<span class="title"> 24/7 Services </span>
					<p>Shop online anytime anyday and pay with great ease.</p>
				</div>
				<div class="card">
					<SVG size="28" type="change" />
					<span class="title"> Exchange Opportunities </span>
					<p>
						Shopping online is easy and convenient with <span> Meji </span>.
					</p>
				</div>
				<div class="card">
					<SVG size="28" type="offer" />
					<span class="title"> More Than Offer </span>
					<p>
						Whatever it is you wish to buy,
						<span> Meji </span> offers you all and lots more at prices which you can trust.
					</p>
				</div>
			</div>
		</section>
	</Body>
</Card>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--gap2);

		text-align: center;
	}

	.first {
		max-width: 300px;
		padding: var(--gap3) 0;

		font-size: large;
	}

	.second {
		display: flex;
		justify-content: center;
		/* align-items: center; */
		flex-direction: column;
		gap: calc(var(--gap2) * 2);

		fill: var(--color1);
	}

	.card {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--gap1);

		max-width: 300px;
	}

	span {
		font-weight: 500;
	}

	@media screen and (min-width: 800px) {
		.first {
			max-width: 500px;
		}
		.second {
			gap: var(--gap3);
			flex-direction: unset;
		}
	}
</style>
