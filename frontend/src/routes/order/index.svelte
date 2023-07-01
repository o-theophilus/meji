<script context="module">
	import { import.meta.env.VITE_BACKEND } from '$lib/store.js';

	export async function load({ fetch, session, url }) {
		if (session.user.login) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order_/${session.user.key}`, {
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
							orders: resp.data.orders
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
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	export let orders;
</script>

<svelte:head>
	<title>Order | Meji</title>
</svelte:head>

<Card>
	<Title title="My Orders" />
	<Body>
		{#each orders as order}
			<div>
				<Button name={`${order.key}`} class="wide" href="/order/{order.key}">
					<div class="fmt">
						{#each order.items as item, i}
							{#if i != 0},{/if}
							{item.name}
						{/each}
					</div>
				</Button>
			</div>
		{:else}
			no order
		{/each}
	</Body>
</Card>

<style>
	.fmt {
		font-weight: normal;
		font-size: smaller;
	}
</style>
