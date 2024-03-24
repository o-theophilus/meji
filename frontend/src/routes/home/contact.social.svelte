<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
</script>

<div class="block">
	<Button class="round large" href="https://wa.me/2348067397793/?text=Hello%20Theophilus" target="_blank">
		<SVG type="whatsapp" />
	</Button>

	<Button class="round large" href="https://twitter.com/o__theophilus" target="_blank">
		<SVG type="twitter" />
	</Button>

	<Button class="round large" href="https://m.facebook.com/o.theophilus" target="_blank">
		<SVG type="facebook" />
	</Button>

	<!-- <Button class="round large" href="https://www.instagram.com/o_theophilus_/" target="_blank" rel="noopener noreferrer">
		<SVG type="instagram" />
	</Button> -->
</div>

<style>
	.block {
		display: flex;
		gap: var(--sp1);
	}
</style>
