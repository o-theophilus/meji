<script>
	let { title, children } = $props();
</script>

<div class="card">
	<div class="title">
		{title}
	</div>

	{@render children?.()}
</div>

<style>
	.card {
		background-color: var(--bg3);
		padding: 16px;
		border-radius: 8px;
	}

	.title {
		color: var(--ft1);
		font-weight: 800;
		font-size: 0.8rem;
		margin-bottom: 8px;
	}
</style>
