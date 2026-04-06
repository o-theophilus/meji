<script>
	let { title, copy } = $props();
</script>

<section>
	<div class="title">
		{@render title?.()}
	</div>
	<div class="copy">
		{@render copy?.()}
	</div>
</section>

<style>
	section {
		padding-top: var(--title-padding-top, 80px);
		padding-bottom: var(--title-padding-bottom, 80px);
		text-align: center;
	}

	.title {
		font-size: 2rem;
		font-weight: 800;
		color: var(--ft1);
		margin: auto;
		max-width: 580px;
	}

	.copy {
		margin: auto;
		font-size: 1.2rem;
		max-width: 580px;
	}
</style>
