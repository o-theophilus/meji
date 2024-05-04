<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import Card from '$lib/card.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Link from '$lib/button/link.svelte';
	import Log from '../../../log/log.svelte';

	export let logs;
	export let voucher_key;
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
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each logs as log (log.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<Log {log} />
				</div>
			{:else}
				<br />
				no item here
			{/each}
		</div>

		<br />
		<Link
			href="/log?{new URLSearchParams(`search=all:voucher:all:${voucher_key}`).toString()}"
			icon
		>
			view more
		</Link>
	{/if}
</Card>

<style>
	.title {
		font-weight: 900;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
</style>
