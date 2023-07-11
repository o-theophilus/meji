<script context="module">
	import { _tick, loading } from '$lib/store.js';

	export async function load({ fetch, session, params, url }) {
		if (session.user.login) {
			loading.set(true);
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order/${params.order}`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: session.token
				}
			});

			if (_resp.ok) {
				loading.set(false);
				let resp = await _resp.json();

				if (resp.status == 200) {
					return {
						props: {
							order: resp.data.order,
							previous_recipients: resp.data.previous_recipients,
							user: session.user
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
	import { user, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';

	import Breakdown from './_comp/breakdown.svelte';
	import Action from './_comp/action.svelte';
	import Status from './_comp/status.svelte';

	import Button from '$lib/button.svelte';
	import Form from './_address.svelte';

	import Address from '$lib/comp/order_address.svelte';
	import Items from '$lib/comp/order_items.svelte';
	import Eta from '$lib/comp/order_eta.svelte';

	export let order;
	export let previous_recipients;
	export let user;
	$: user = $user ? $user : user;

	$: if ($_tick) {
		order = $_tick;
		$_tick = '';
	}
</script>

<svelte:head>
	<title>Order | Meji</title>
</svelte:head>

<Card>
	<Title title="Order ID: {order.key}" />
</Card>
<section>
	<div class="block">
		{#if order.status != 'delivered'}
			<Eta {order} />
		{/if}
		<Address {order} let:complete_address>
			{#if order.status == 'pending'}
				<Button
					class={!complete_address ? 'primary' : ''}
					icon="edit"
					on:click={() => {
						$module = {
							module: Form,
							data: {
								order,
								previous_recipients
							}
						};
					}}
				/>
			{/if}
		</Address>
	</div>
	<div class="block">
		{#if order.status == 'pending'}
			<Breakdown {user} {order} />
			<Action {order} />
		{:else}
			<Items {order} />
			<Status {order} />
		{/if}
	</div>
</section>

<style>
	section,
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		width: 100%;
	}
	section {
		margin-top: var(--sp2);
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
		}
	}
</style>
