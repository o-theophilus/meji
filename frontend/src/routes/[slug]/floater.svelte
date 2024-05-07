<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';
	import Add_Cart from '$lib/item/add_cart.svelte';
	import Share from './floater_share.svelte';

	export let item = {};
</script>

<div class="floater">
	<div class="row">
		<div class="row">
			<Add_Cart {item} />
			<Button
				href="https://api.whatsapp.com/send?phone=+2348067397793&text=Hi%0AI want to make enquiry concerning ${item.name} on Meji.ng%20{$page
					.url.href}"
				target="_blank"
			>
				<SVG icon="whatsapp" />
				Chat
			</Button>
		</div>
		<BRound
			icon="share"
			on:click={() => {
				$module = {
					module: Share,
					item
				};
			}}
		/>
	</div>
</div>

<style>
	.row {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.floater {
		position: sticky;
		bottom: var(--headerHeight);
		padding: var(--sp2) 0;

		/* bottom: calc(var(--headerHeight) + var(--sp2));

		padding-top: var(--sp2); */
		border-top: 2px solid var(--ac4);

		background-color: var(--ac6);
	}

	@media screen and (min-width: 800px) {
		.floater {
			bottom: 0;
		}
	}
</style>
