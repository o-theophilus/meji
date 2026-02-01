<script>
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
</script>

<div class="block">
	<div class="page_title">What are you waiting for?</div>
	<div class="text">The best deals are just a click away.</div>
	<Button icon2="arrow-right" href="/shop" --button-width="fit-content" --button-font-size="1.2rem">
		Shop Now
	</Button>
</div>

<style>
	.block {
		margin: 80px 0;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: 16px;

		padding: 0 16px;
		text-align: center;

		& .page_title {
			font-size: 2rem;
		}
		& .text {
			max-width: 740px;
		}
	}
</style>
