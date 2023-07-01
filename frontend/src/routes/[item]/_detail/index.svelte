<script>
	import Img from './photo.svelte';
	import Info from './info.svelte';
	import Desc from './desc.svelte';
	import Spec from './spec.svelte';
	import Feedback from './feedback.svelte';
	import Meta from './meta.svelte';
	import Floater from './floater.svelte';
	import Card from '$lib/comp/card.svelte';

	export let item;
</script>

<Meta title={item.name} description={item.desc} image={item.thumbnail} />

<section class="details">
	<div class="block left">
		<Img {item} />
	</div>
	<div class="block">
		<Card>
			<div class="block2">
				<Info {item} />
				<Desc {item} />
				<Spec {item} />
				<Feedback {item} />
				<Floater {item} />
			</div>
		</Card>
		<slot />
	</div>
</section>

<style>
	.details {
		gap: var(--gap1);
		display: flex;
		flex-direction: column;
	}
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--gap3);

		width: 100%;
	}

	@media screen and (min-width: 800px) {
		.details {
			flex-direction: unset;
			position: relative;
		}

		.left {
			position: sticky;
			top: var(--gap1);

			align-self: flex-start;
		}
	}
</style>
