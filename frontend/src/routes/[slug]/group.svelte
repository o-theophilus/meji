<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import ButtonFold from '$lib/button.fold.svelte';

	export let name = 'Group Name';
	export let url;
	let items = [];
	let open = true;

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}${url}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			items = resp.items;
		} else {
			error = resp;
		}
	});
</script>

{#if items && items.length > 0}
	<Card>
		<div class="title">
			{name}
			<ButtonFold
				{open}
				on:click={() => {
					open = !open;
				}}
			/>
		</div>

		{#if open}
			<div
				class="item_area"
				class:list={$user.setting.item_view == 'list'}
				transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}
			>
				{#each items as x (x.key)}
					<Item item={x} />
				{/each}
			</div>
		{/if}
	</Card>
{/if}

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
</style>
