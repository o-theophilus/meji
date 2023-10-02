<script>
	import { token } from '$lib/cookie.js';
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';

	import Card from '$lib/card.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Log from '../../../logs/log.svelte';
	import { onMount } from 'svelte';

	export let voucher_key;
	let logs = [];
	let loading = true;

	onMount(async () => {
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/logs?search=all:voucher:all:${voucher_key}&size=9999`,
			{
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				}
			}
		);
		resp = await resp.json();
		loading = false;

		if (resp.status == 200) {
			logs = resp.logs;
		}
	});

	let open = false;
</script>

<Card>
	<div class="title">
		Log{logs.length > 1 ? 's' : ''}
		<ButtonFold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	</div>

	{#if open}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
			{#if loading}
			<br />
				Loading . . .
			{:else}
				{#each logs as log}
					<Log {log} />
				{:else}
					<br />
					no item here
				{/each}
			{/if}
		</div>
	{/if}
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
</style>
