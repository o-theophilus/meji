<script>
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';

	export let order;
</script>

<Card>
	<Title title="Items" />
	<Body>
		<div class="grid">
			<div class="th">name</div>
			<div class="th">qty</div>
			{#each order.items as item, i}
				<div class="text">
					<a href="/{item.alias}">
						{item.name}
					</a>
				</div>
				<div class="num">
					{item.quantity}
				</div>
			{/each}
		</div>
	</Body>
</Card>

<style>
	.grid {
		display: grid;
		gap: var(--gap1) var(--gap3);
		grid-template-columns: 1fr auto;
	}

	.th {
		font-weight: 500;
	}

	.num {
		text-align: center;
	}
	a {
		color: var(--font1);
		text-decoration: none;
	}
</style>
