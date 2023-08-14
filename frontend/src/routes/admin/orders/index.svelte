<script context="module">
	import { get_query } from '$lib/page_state.js';

	export async function load({ fetch, session, url }) {
		if (session.user.login) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order${get_query('orders')}`, {
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
							orders: resp.data.orders,
							total_page: resp.data.total_page
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
	import { token } from '$lib/cookie.js';
	import { state } from '$lib/page_state.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import Search from '$lib/comp/search.svelte';
	import Status from '$lib/comp/status_bar.svelte';
	import Pagination from '$lib/comp/pagination.svelte';

	export let orders = [];
	export let total_page = 1;

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order${get_query('orders')}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				orders = resp.data.orders;
				total_page = resp.data.total_page;
			} else {
				error = resp.message;
			}
		}
	};

	let pagination;

	let bar_items = [
		{ name: 'pending', icon: 'none' },
		{ name: 'ordered', icon: 'none' },
		{ name: 'processing', icon: 'none' },
		{ name: 'enroute', icon: 'none' },
		{ name: 'delivered', icon: 'none' },
		{ name: 'cancelled', icon: 'none' }
	];
</script>

<svelte:head>
	<title>Order | Meji</title>
</svelte:head>

<Card>
	Orders

	<Search
		on:ok={() => {
			pagination.init();
			submit();
		}}
	/>

	<Status
		{bar_items}
		on:ok={() => {
			pagination.init();
			submit();
		}}
	>
		<svelte:fragment slot="before">
			<Button
				name="all"
				class="tiny"
				active={!$state.orders.status}
				on:click={() => {
					$state.orders.status = '';
					pagination.init();
					submit();
				}}
			/>
		</svelte:fragment>
	</Status>

	{#each orders as order}
		<div>
			<Button name={`${order.key}`} class="wide" href="order/{order.key}">
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

	<svelte:component
		this={Pagination}
		bind:this={pagination}
		{total_page}
		on:ok={(e) => {
			submit();
		}}
	/>
</Card>

<style>
	.fmt {
		font-weight: normal;
		font-size: smaller;
	}
</style>
