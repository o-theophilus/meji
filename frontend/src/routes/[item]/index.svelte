<script context="module">
	import { loading } from '$lib/store.js';

	export async function load({ fetch, session, params }) {
		loading.set(true);
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}item_info/${params.item}`, {
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
						item: resp.data.item,
						group: resp.data.group
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
</script>

<script>
	import { _tick } from '$lib/store.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Item from '$lib/comp/item.svelte';

	import Detail from './_detail/index.svelte';

	export let item;
	export let group = [];

	$: if ($_tick) {
		item = $_tick;
		$_tick = '';
	}
</script>

<svelte:head>
	<title>{item.name} | Meji</title>
</svelte:head>

<section class="whole">
	<Detail {item} />

	{#if group.length > 0}
		<section>
			{#each group as x}
				{#if x.items && x.items.length > 0}
					<Card>
						<Title title={x.name} />
						<Body grid>
							{#each x.items as item (item.key)}
								<Item {item} />
							{/each}
						</Body>
					</Card>
				{/if}
			{/each}
		</section>
	{/if}
</section>

<style>
	.whole {
		display: grid;
		gap: var(--gap3);
	}
</style>
