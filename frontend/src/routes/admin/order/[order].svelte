<script context="module">
	import { import.meta.env.VITE_BACKEND } from '$lib/store.js';

	export async function load({ fetch, session, params, url }) {
		if (session.user.login) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order/${params.order}`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: session.token
				}
			});

			if (_resp.ok) {
				let resp = await _resp.json();

				if (resp.status == 200) {
					return {
						props: {
							order: resp.data.order
						}
					};
				} else {
					return {
						status: 404,
						error: resp.message
					};
				}
			}
		}
		return {
			status: 302,
			redirect: `/?module=login&return_url=${url.pathname}`
		};
	}
</script>

<script>
	import { _tick } from '$lib/store.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';

	import Address from '$lib/comp/order_address.svelte';
	import Items from '$lib/comp/order_items.svelte';
	import Eta from '$lib/comp/order_eta.svelte';

	import Admin from './_admin.svelte';

	export let order;

	$: if ($_tick) {
		order = $_tick;
		$_tick = '';
	}
</script>

<svelte:head>
	<title>Order | Meji</title>
</svelte:head>

<Card>
	<Title title={order.key} />
</Card>
<section>
	<div class="wide">
		<Eta {order} admin />
		<Items {order} />
		<Address {order} />
	</div>

	<div class="wide">
		<Card>
			<Title title="Payment" />
			<Body>
				<div>
					<span> Cost </span>
					<br />
					Total items: {order.info.total_items}
					<br />
					Delivery: {order.info.delivery_fee}
				</div>
				<div>
					<span> Payment </span>
					<br />
					Paid: {order.info.delivery_fee + order.info.total_items}
					<br />
					Account: {order.info.account}
				</div>
			</Body>
		</Card>

		<Admin
			{order}
			on:ok={(e) => {
				order = e.detail;
			}}
		/>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap1);

		margin-top: var(--gap1);
	}

	.wide {
		display: flex;
		flex-direction: column;
		gap: var(--gap1);

		width: 100%;
	}

	span {
		font-weight: 500;
	}
	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
			/* gap: var(--gap1); */
		}
	}
</style>
