<script>
	import { Button } from '$lib/button';
</script>

<div class="margin center">
	<div class="title">What are you waiting for?</div>
	<br />
	<div class="text">The best deals are just a click away.</div>
	<br />
	<Button
		--button-background-color="var(--cl3)"
		--button-background-color-hover="var(--cl3_)"
		--button-color="white"
		--button-outline-color="transparent"
		href="/shop"
		icon2="arrow-right"
	>
		Shop Now
	</Button>
</div>

<style>
	.margin {
		margin: 160px 0;
	}

	.title {
		font-size: 2rem;
		color: var(--ft1);
		line-height: 120%;
		font-weight: 600;
	}

	.center {
		text-align: center;
	}
</style>
