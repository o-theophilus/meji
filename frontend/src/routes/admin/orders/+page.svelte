<script>
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Meta from '$lib/meta.svelte';

	export let data;
	let { orders } = data;
</script>

<Meta title="Order" description="Order" />

<Card>
	<b> My Orders </b>
	<br />
	<br />
	{#each orders as x}
		<div>
			<Button name={`${x.key}`} class="wide" href="/profile/orders/{x.key}">
				<div class="fmt">
					{#each x.items as y, i}
						{#if i != 0},{/if}
						{y.name}
					{/each}
				</div>
			</Button>
		</div>
	{:else}
		no item here
	{/each}
</Card>

<style>
	.fmt {
		font-weight: normal;
		font-size: smaller;
	}
</style>
