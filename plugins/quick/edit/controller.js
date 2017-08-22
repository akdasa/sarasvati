function update(save) {
    if (typeof(save) === "undefined") save = true;
    self.changed(title.text, description.text, save)
}
