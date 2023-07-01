<script>
	export let title;
	export let color = false;
</script>

<div class="divider" />

<section>
	<div class="title" class:color>{title}</div>
	<div class="right"><slot /></div>
</section>

<style>
	.divider:not(:first-child) {
		height: 2px;
		background-color: var(--background);
		margin: 0 var(--gap2);
	}

	section {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--gap2);

		padding: var(--gap2);
	}
	.title {
		font-weight: bold;
		color: var(--font1);
	}
	.color {
		color: var(--color1);
	}
	.right {
		display: flex;
		align-items: center;
		gap: var(--gap1);

		flex-shrink: 0;
	}
</style>
